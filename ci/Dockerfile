FROM python:3.12.3

WORKDIR /pipeline
ADD requirements.txt /pipeline
RUN pip install -r requirements.txt

ADD . /pipeline

CMD ["python", "start_lightning_job.py"]
