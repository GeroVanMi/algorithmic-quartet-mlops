FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Install gcloud CLI & Python
RUN apt update -y
RUN apt install apt-transport-https ca-certificates gnupg curl python3 python3-pip python3-venv -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt update -y && apt install google-cloud-sdk -y

WORKDIR /root

# If we install python packages with the global pip we run the risk 
# of breaking the system, since it can depend on certain libraries.
# Therefore, we use a virtual environment for it.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install python libraries
ADD ./requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

# Add the project files and run the pipeline
ADD . /root
CMD [ "bash", "run_pipeline.sh" ]
