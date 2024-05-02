import argparse

import torch
from configurations.Configuration import Configuration
from configurations.create_config import create_config_from_arguments
from configurations.DevConfig import DevConfig
from configurations.WandBConfig import WandB
from data_utilities.load_bucket import download_bucket_with_transfer_manager
from datasets import load_dataset
from diffusers.models.unets.unet_2d import UNet2DModel
from diffusers.optimization import get_cosine_schedule_with_warmup
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from torch.utils.data.dataloader import DataLoader
from torchvision import transforms
from train import train_loop


def prepare_data(config: Configuration):
    if isinstance(config, DevConfig):
        print("Testing Training pipeline. This will not train the model!")
        print("In order to train the model, pass the -t or --training flag!")

        if not config.local_dataset_path.exists():
            download_bucket_with_transfer_manager(
                config.training_bucket_name, max_results=config.num_images
            )

        return load_dataset(
            str(config.local_dataset_path.resolve()), split="train[0:6]"
        )

    if not config.local_dataset_path.exists():
        download_bucket_with_transfer_manager(config.training_bucket_name)

        return load_dataset(str(config.local_dataset_path.resolve()))


def run_pipeline(config: Configuration):
    dataset = prepare_data(config)
    wandb_config = WandB(
        project_name="Training",
        entity="algorithmic-quartet-zhaw",
        mode="training",
    )
    wandb_config.create_run("Train Model")

    preprocess = transforms.Compose(
        [
            transforms.Resize((config.image_size, config.image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ]
    )

    def transform(examples):
        images = [preprocess(image.convert("RGB")) for image in examples["image"]]
        return {"images": images}

    dataset.set_transform(transform)  # type: ignore Type definitions are incorrect

    train_dataloader = DataLoader(
        dataset,  # type: ignore Type definitions are incorrect
        batch_size=config.train_batch_size,
        shuffle=True,
    )
    model = UNet2DModel(
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

    noise_scheduler = DDPMScheduler(num_train_timesteps=config.number_of_noise_steps)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    lr_scheduler = get_cosine_schedule_with_warmup(
        optimizer=optimizer,
        num_warmup_steps=config.lr_warmup_steps,
        num_training_steps=(len(train_dataloader) * config.num_epochs),
    )

    train_loop(
        config,
        model,
        noise_scheduler,
        optimizer,
        train_dataloader,
        lr_scheduler,
        wandb_config,
    )


if __name__ == "__main__":
    config = create_config_from_arguments()
    run_pipeline(config)
