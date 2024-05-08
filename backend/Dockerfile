FROM python:3.12

# Install gcloud CLI & Python
RUN apt update -y
RUN apt install apt-transport-https ca-certificates gnupg curl python3 python3-pip python3-venv -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt update -y && apt install google-cloud-sdk -y
WORKDIR /server

# Install python packages
ADD ./requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt

# Copy code
ADD . /server

# Run FastAPI server
CMD ["python", "app.py"]

