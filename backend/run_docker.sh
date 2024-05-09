#!/bin/bash

docker build -t fastapi .
docker run -it -e CLOUD_BUCKET -e WANDB_API_KEY -p 8000:8000 fastapi
