FROM python:3.12

WORKDIR /server

# Install python packages
ADD ./requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt

# Copy code 
ADD . /server

# Run FastAPI server
CMD ["python", "app.py"]

