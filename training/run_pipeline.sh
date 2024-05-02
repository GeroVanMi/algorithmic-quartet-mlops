#!/bin/bash
set -e 
# W&B Login
wandb login $WANDB_API_KEY

# Google Cloud Service Account Login
mkdir -p ~/.config/gcloud/
echo $GC_BUCKET_KEY > ~/.config/gcloud/application_default_credentials.json
gcloud auth application-default login lightning-ci@algorithmic-quartet.iam.gserviceaccount.com

python $PWD/pipeline.py