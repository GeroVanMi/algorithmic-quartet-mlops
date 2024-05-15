import os

from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    studio = create_studio()

    print("Starting studio.")
    studio.start(Machine.T4_X_4)

    BASE_PATH = "/teamspace/studios/this_studio/algorithmic-quartet-mlops"

    print("Logging into Google Cloud Artifact registry with docker.")
    studio.run(
        "cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://us-west2-docker.pkg.dev"
    )

    print("Running training docker container...")
    # TODO: The environment variables should be stored in an ENV file and passed to the container like that to prevent them from being logged to the terminal.

    # studio.run(
    #     f"echo '{os.environ.get('WANDB_API_KEY')}' > ~/.env && echo '{os.environ.get('GC_BUCKET_KEY')}' >> ~/.env"
    # )
    studio.run(
        "docker pull us-west2-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest"
    )

    studio.run(
        f"docker run -d --gpus all -e TAG_NAME -e WANDB_API_KEY='{os.environ.get('WANDB_API_KEY')}' -e GC_BUCKET_KEY='{os.environ.get('GC_BUCKET_KEY')}' us-west2-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest"
    )
