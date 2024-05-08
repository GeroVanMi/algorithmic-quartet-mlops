#!/bin/bash

docker build -t fastapi .
docker run -it -e CLOUD_BUCKET -e WANDB_API_KEY -p 8003:8001 fastapi
