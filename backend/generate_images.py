import os
import time
from pathlib import Path

import torch
import wandb
from accelerate import Accelerator
from Configuration import Configuration
from diffusers.models.unets.unet_2d import UNet2DModel
from diffusers.pipelines.ddpm.pipeline_ddpm import DDPMPipeline
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from google.cloud import storage
from google.cloud.storage import Client, transfer_manager
from PIL.Image import Image


# TODO: This code should be imported from `training/src/model/create_model`
# But python is a terrible language that doesn't allow importing from neighboring folders so I guess we just copy+paste?
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
        current_time = time.time()
        image.save(f"{predictions_directory}/{current_time}_{index:0>2}.png")


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


def upload_directory_with_transfer_manager(
    bucket_name="zhaw_algorithmic_quartet_generated_images",
    source_directory="./predictions",
    workers=8,
):
    """Upload every file in a directory, including all files in subdirectories.

    Each blob name is derived from the filename, not including the `directory`
    parameter itself. For complete control of the blob name for each file (and
    other aspects of individual blob metadata), use
    transfer_manager.upload_many() instead.
    """

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)

    # First, recursively get all files in `directory` as Path objects.
    directory_as_path_obj = Path(source_directory)
    paths = directory_as_path_obj.rglob("*")

    # Filter so the list only includes files, not directories themselves.
    file_paths = [path for path in paths if path.is_file()]

    # These paths are relative to the current working directory. Next, make them
    # relative to `directory`
    relative_paths = [path.relative_to(source_directory) for path in file_paths]

    # Finally, convert them all to strings.
    string_paths = [str(path) for path in relative_paths]

    print("Found {} files.".format(len(string_paths)))

    # Start the upload.
    results = transfer_manager.upload_many_from_filenames(
        bucket, string_paths, source_directory=source_directory, max_workers=workers
    )

    for name, result in zip(string_paths, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))


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
