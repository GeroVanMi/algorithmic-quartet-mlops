from dataclasses import dataclass
from pathlib import Path


@dataclass
class Configuration:
    image_size = 128  # the generated image resolution
    gradient_accumulation_steps = 1
    mixed_precision = "fp16"  # `no` for float32, `fp16` for automatic mixed precision

    project_dir = Path(__file__).parents[1]

    wandb_project = "Training"
    wandb_entity = "algorithmic-quartet-zhaw"

    model_name = "pokemon-generator"
    artifact_name = f"{wandb_entity}/model-registry/{model_name}:latest"
    output_dir = project_dir.joinpath(f"models/{model_name}")

    overwrite_output_dir = True  # overwrite the old model when re-running the notebook
    seed = 0
    number_of_noise_steps = 2  # Set to 1000 for training

    eval_batch_size = 2
