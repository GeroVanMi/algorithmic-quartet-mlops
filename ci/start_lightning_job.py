import os

from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    studio = create_studio()

    print("Starting studio.")
    studio.start(machine=Machine.CPU)

    BASE_PATH = "/teamspace/studios/this_studio/algorithmic-quartet-mlops"

    # Use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    # 1. Log in to the artifact registry
    # 2. Pull the docker image from the registry
    # 3. Run the docker container with GPUs and the appropriate environment variables
    training_command = f"""
        cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://us-west2-docker.pkg.dev && \
        docker pull us-west2-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest && \
        docker run --gpus all -e WANDB_API_KEY='{os.environ.get('WANDB_API_KEY')}' -e GC_BUCKET_KEY='{os.environ.get('GC_BUCKET_KEY')}' us-west2-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest
    """
    print("Starting studio job.")
    jobs_plugin.run(command=training_command, name="Traing model", machine=Machine.T4)  # type: ignore

    print("Saving state and quitting...")
    studio.stop()
