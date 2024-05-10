#!/bin/bash

set -a
source .env

docker build -t streamlit_frontend .
docker run --net=host -it -e CLOUD_BUCKET -e WANDB_API_KEY -p 8501:8501 streamlit_frontend
