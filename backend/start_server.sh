#!/bin/bash

# Google Cloud Service Account Login
mkdir -p ~/.config/gcloud/
echo $CLOUD_BUCKET > ~/.config/gcloud/application_default_credentials.json
gcloud auth application-default login fastapi@algorithmic-quartet.iam.gserviceaccount.com
wandb login $WANDB_API_KEY

fastapi run $PWD/src/app.py --port 8000
