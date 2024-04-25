from dataclasses import dataclass
from pathlib import Path


@dataclass
class Configuration:
    image_size = 128  # the generated image resolution
    gradient_accumulation_steps = 1
    learning_rate = 1e-4
    lr_warmup_steps = 500
    save_image_epochs = 10
    save_model_epochs = 30
    mixed_precision = "fp16"  # `no` for float32, `fp16` for automatic mixed precision

    local_dataset_path = Path("./data/")
    training_bucket_name = "zhaw_algorithmic_quartet_training_images"

    output_dir = "./models/ddpm-pokemon-128"

    push_to_hub = False  # whether to upload the saved model to the HF Hub
    hub_private_repo = False
    overwrite_output_dir = True  # overwrite the old model when re-running the notebook
    seed = 0
    number_of_noise_steps = 5  # Set to 1000 for training

    # These values are overwritten by the Dev / Train Configs
    train_batch_size = 2
    eval_batch_size = 16
    num_epochs = 2
