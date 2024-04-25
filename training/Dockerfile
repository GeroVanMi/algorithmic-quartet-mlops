FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

# Install gcloud CLI 
RUN apt update -y
RUN apt install apt-transport-https ca-certificates gnupg curl -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt update -y && apt install google-cloud-sdk -y

WORKDIR /root

ADD ./requirements.txt /root/requirements.txt
# We really want to re-use the libraries here
# RUN python3 -m venv /root/venv/
# RUN source /root/venv/bin/activate
RUN pip install -r requirements.txt
ADD . /root
