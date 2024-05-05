import os
from pathlib import Path

import torch
from accelerate import Accelerator
from Configuration import Configuration
from diffusers.models.unets.unet_2d import UNet2DModel
from diffusers.pipelines.ddpm.pipeline_ddpm import DDPMPipeline
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from diffusers.utils.pil_utils import make_image_grid


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


def prediction():
    config = Configuration()
    accelerator = Accelerator(
        mixed_precision=config.mixed_precision,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        log_with="tensorboard",
        project_dir=os.path.join(config.output_dir, "logs"),
    )

    noise_scheduler = DDPMScheduler(num_train_timesteps=config.number_of_noise_steps)
    model = create_model(config)
    pipeline = DDPMPipeline(
        unet=accelerator.unwrap_model(model), scheduler=noise_scheduler
    )
    # TODO: Download pipeline files from W&B model registry
    pipeline.from_pretrained("../training/models/pokemon-generator/")

    images = pipeline(
        batch_size=config.eval_batch_size,
        generator=torch.manual_seed(config.seed),
        num_inference_steps=config.number_of_noise_steps,  # TODO: This needs to be set via the config and synced with the training equivalent
    ).images  # type: ignore

    # Make a grid out of the images
    image_grid = make_image_grid(images, rows=4, cols=4)  # type: ignore

    # Save the images
    predictions_directory = Path("predictions/")
    os.makedirs(predictions_directory, exist_ok=True)

    # TODO: Store images in the cloud bucket
    image_grid.save(f"{predictions_directory}/new_images.png")


if __name__ == "__main__":
    prediction()
