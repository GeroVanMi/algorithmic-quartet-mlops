# Algorithmic Quartet Image Generation

Building a Pokemon Image Generator with MLOps best practices!

![Flow Chart of the pipeline](flow_chart.png)

## Training Pipeline

The training is done with PyTorch and HuggingFace on Lightning.ai Studios.
The data for it is stored on a GCP Cloud Bucket and downloaded to the GPU device for training.

## Frontend

The frontend is a streamlit UI that renders the generated images.  
It is continously deployed with GCP Cloud Build and is live on a GCP Cloud Run instance.

## Backend

The image generation service uses FastAPI to serve the latest trained model and runs on a GCP Cloud Run instance.

## Automated training & Continous Delivery

Autmated Training is described best in this video: https://vimeo.com/948396185

The Frontend and Backend are both built and deployed automatically when a Git Tag is added to a certain commit with either a `frontend/VERSION` or `backend/VERSION`.
