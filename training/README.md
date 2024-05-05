# Training Pipeline

## Installation

To run the pipeline locally, we recommend creating a python virtual environment.

```bash
# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the project dependencies
pip install -r requirements.txt
```

Then you can run the pipeline script:

```bash
python src/pipeline.py
```

It will prompt you to provide a W&B account and you will
need to authenticate with Google Cloud to have access to the bucket.

Alternatively, you can download your images directly to `./data/`
