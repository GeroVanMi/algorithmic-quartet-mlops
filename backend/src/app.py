from fastapi import FastAPI
from pydantic import BaseModel
from src.Configuration import Configuration
from src.download_pipeline import download_pipeline_files
from src.generate_images import *
from src.save_model_rating import wandb_rate_model

app = FastAPI()
config = Configuration()

model_id = download_pipeline_files(config)


class RatingBody(BaseModel):
    rating: int


@app.post("/rate_model")
def rate_model(rating: RatingBody):
    wandb_rate_model(model_id, rating.rating, config)
    return "Rating submitted."


@app.get("/generate_images")
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
        upload_directory_with_transfer_manager()

    return model_id
