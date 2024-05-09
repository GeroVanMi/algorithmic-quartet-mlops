#!/bin/bash

# Google Cloud Service Account Login
set -a
mkdir -p ~/.config/gcloud/
echo $CLOUD_BUCKET > ~/.config/gcloud/application_default_credentials.json
gcloud auth application-default login fastapi@algorithmic-quartet.iam.gserviceaccount.com

streamlit run streamlit_ui.py
