FROM python:3.10-bookworm

# Set working directory
WORKDIR /frontend

RUN apt update -y
RUN apt install apt-transport-https ca-certificates gnupg curl -y
RUN apt install python3 python3-pip -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt update -y && apt install google-cloud-sdk -y

# Copy the current directory contents
ADD requirements.txt /frontend
RUN pip install -r requirements.txt
ADD . /frontend
RUN mkdir -p ~/.config/gcloud
RUN cp keys/gc.json ~/.config/gcloud/application_default_credentials.json
RUN gcloud auth application-default login lightning-ci@algorithmic-quartet.iam.gserviceaccount.com

# Make port 8501 available to the world
EXPOSE 8501

# Run streamlit_ui.py when the container launches
CMD ["streamlit", "run", "streamlit_ui.py"]
#CMD ["bash"] # For issue fights