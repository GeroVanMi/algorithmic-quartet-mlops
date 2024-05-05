import torch
from configurations import (
    Configuration,
    TrainConfig,
    WandB,
    create_config_from_arguments,
)
from data_utilities.cloud_bucket import prepare_data
from diffusers.optimization import get_cosine_schedule_with_warmup
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from model.create_model import create_model
from torch.utils.data.dataloader import DataLoader
from torchvision import transforms
from train import train_loop


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
    model = create_model(config)
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

    if isinstance(config, TrainConfig):
        wandb_config.link_model(
            config.output_dir,
            config.model_name,
        )


if __name__ == "__main__":
    config = create_config_from_arguments()
    run_pipeline(config)
