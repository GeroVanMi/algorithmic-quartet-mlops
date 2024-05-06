import os

from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    studio = create_studio()

    print(studio.status)
    if studio.status != "Status.Running":
        print("Starting studio.")
        studio.start(Machine.T4)
    else:
        print("Studio is already running. Not starting it again.")

    BASE_PATH = "/teamspace/studios/this_studio/algorithmic-quartet-mlops"

    # Use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    # Start the training pipeline on a GPU job
    # cmd = f"""cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://europe-west1-docker.pkg.dev && \
    # docker run --gpus all europe-west1-docker.pkg.dev/algorithmic-quartet/training-pipelines/pokemon-trainer:latest
    # """
    # studio.run(f'export WANDB_API_KEY={os.environ.get("WANDB_API_KEY")}')
    # studio.run(f'export GC_BUCKET_KEY=\'{os.environ.get("GC_BUCKET_KEY")}\'')

    print("Logging into Google Cloud Artifact registry with docker.")
    studio.run(
        "cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://europe-west1-docker.pkg.dev"
    )

    print("Running training docker container...")
    # TODO: The environment variables should be stored in an ENV file and passed to the container like that to prevent them from being logged to the terminal.

    # studio.run(
    #     f"echo '{os.environ.get('WANDB_API_KEY')}' > ~/.env && echo '{os.environ.get('GC_BUCKET_KEY')}' >> ~/.env"
    # )
    studio.run(
        "docker pull europe-west1-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest"
    )

    studio.run(
        f"docker run --gpus all -e WANDB_API_KEY='{os.environ.get('WANDB_API_KEY')}' -e GC_BUCKET_KEY='{os.environ.get('GC_BUCKET_KEY')}' europe-west1-docker.pkg.dev/algorithmic-quartet/training-images/pokemon-trainer:latest"
    )
    # studio.run("rm ~/.env")

    print("Saving state and quitting...")
    studio.stop()
