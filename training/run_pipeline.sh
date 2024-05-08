#!/bin/bash
set -e 
# W&B Login
echo $WANDB_API_KEY
wandb login $WANDB_API_KEY

# Google Cloud Service Account Login
mkdir -p ~/.config/gcloud/
echo $GC_BUCKET_KEY > ~/.config/gcloud/application_default_credentials.json
gcloud auth application-default login lightning-ci@algorithmic-quartet.iam.gserviceaccount.com

python $PWD/src/pipeline.py
python $PWD/stop_studio.py

