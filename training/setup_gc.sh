# Install gcloud cli
# TODO: Do we need to do this every single time? 
sudo apt update -y
sudo apt install apt-transport-https ca-certificates gnupg curl -y
sudo apt install python3 python3-pip -y
sudo echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg &&\
  sudo apt update -y && sudo apt install google-cloud-sdk -y


# Create the config folder
mkdir -p ~/.config/gcloud/

# Copy the credentials file to the folder
# TODO: This should be replaced with environments variables and secrets?
cp ~/algorithmic-quartet/training/keys/gc.json ~/.config/gcloud/application_default_credentials.json

# Setup the gcloud authentication
gcloud auth application-default login lightning-ci@algorithmic-quartet.iam.gserviceaccount.com
