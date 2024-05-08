from dataclasses import dataclass
from pathlib import Path


@dataclass
class Configuration:
    image_size = 128  # the generated image resolution
    gradient_accumulation_steps = 1
    mixed_precision = "fp16"  # `no` for float32, `fp16` for automatic mixed precision

    local_dataset_path = Path("./data/")
    training_bucket_name = "zhaw_algorithmic_quartet_training_images"

    model_name = "pokemon-generator"
    output_dir = f"./models/{model_name}"

    overwrite_output_dir = True  # overwrite the old model when re-running the notebook
    seed = 0
    number_of_noise_steps = 100  # Set to 1000 for training

    eval_batch_size = 16
