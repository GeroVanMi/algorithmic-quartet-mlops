import os
from pathlib import Path

import torch
import wandb
from accelerate import Accelerator
from Configuration import Configuration
from diffusers.models.unets.unet_2d import UNet2DModel
from diffusers.pipelines.ddpm.pipeline_ddpm import DDPMPipeline
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from PIL.Image import Image


# TODO: This code should be imported from `training/src/model/create_model`
def create_model(config: Configuration):
    return UNet2DModel(
        sample_size=config.image_size,  # the target image resolution
        in_channels=3,  # the number of input channels, 3 for RGB images
        out_channels=3,  # the number of output channels
        layers_per_block=2,  # how many ResNet layers to use per UNet block
        block_out_channels=(
            128,
            128,
            256,
            256,
            512,
            512,
        ),  # the number of output channels for each UNet block
        down_block_types=(
            "DownBlock2D",  # a regular ResNet downsampling block
            "DownBlock2D",
            "DownBlock2D",
            "DownBlock2D",
            "AttnDownBlock2D",  # a ResNet downsampling block with spatial self-attention
            "DownBlock2D",
        ),
        up_block_types=(
            "UpBlock2D",  # a regular ResNet upsampling block
            "AttnUpBlock2D",  # a ResNet upsampling block with spatial self-attention
            "UpBlock2D",
            "UpBlock2D",
            "UpBlock2D",
            "UpBlock2D",
        ),
    )


def save_images(images: list[Image]):
    # TODO: Store images in the cloud bucket
    predictions_directory = Path("predictions/")
    os.makedirs(predictions_directory, exist_ok=True)

    for index, image in enumerate(images):
        image.save(f"{predictions_directory}/{index:0>2}.png")


def initialize_pipeline(accelerator, config) -> DDPMPipeline:
    run = wandb.init()
    if run is None:
        raise RuntimeError("Couldn't initalize W&B!")

    artifact = run.use_artifact(
        "algorithmic-quartet-zhaw/model-registry/pokemon-generator:latest", type="model"
    )
    model_path = Path("model/pokemon-generator")
    artifact.download(root=model_path)

    noise_scheduler = DDPMScheduler(num_train_timesteps=config.number_of_noise_steps)
    model = create_model(config)
    pipeline = DDPMPipeline(
        unet=accelerator.unwrap_model(model), scheduler=noise_scheduler
    )
    return pipeline.from_pretrained(model_path)  # type: ignore (There are multiple definitions which break the type hints)


def generate_images():
    config = Configuration()
    accelerator = Accelerator(
        mixed_precision=config.mixed_precision,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        log_with="tensorboard",
        project_dir=os.path.join(config.output_dir, "logs"),
    )

    image_generation_pipeline = initialize_pipeline(accelerator, config)

    images = image_generation_pipeline(
        batch_size=config.eval_batch_size,
        generator=torch.manual_seed(config.seed),
        num_inference_steps=config.number_of_noise_steps,
    ).images  # type: ignore (There are multiple definitions which break the type hints)

    if isinstance(images, list):
        save_images(images)


if __name__ == "__main__":
    generate_images()
