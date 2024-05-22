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
def handle_generate_images():
    config = Configuration()
    images = generate_images(config)

    if isinstance(images, list):
        save_images(images)
        upload_directory_with_transfer_manager()

    return model_id
