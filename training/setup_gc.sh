# Create the config folder
mkdir /root/.config/
mkdir /root/.config/gcloud/

# Copy the credentials file to the folder
# TODO: This should be replaced with environments variables and secrets?
cp /root/gc.json /root/.config/gcloud/application_default_credentials.json

# Setup the gcloud authentication
gcloud auth application-default login lightning-ci@algorithmic-quartet.iam.gserviceaccount.com
