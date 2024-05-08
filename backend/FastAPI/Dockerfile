FROM python:3.12
WORKDIR /server
ADD ./requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt
ADD . /server
CMD ["python", "app.py"]

