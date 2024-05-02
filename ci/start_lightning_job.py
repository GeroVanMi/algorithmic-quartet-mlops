import os

from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    studio = create_studio()

    if studio.status != "Status.Running":
        print("Starting studio.")
        studio.start()
    else:
        print("Studio is already running. Not starting it again.")

    BASE_PATH = "/teamspace/studios/this_studio/algorithmic-quartet-mlops"

    # Use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    # Start the training pipeline on a GPU job
    # cmd = f"""cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://europe-west9-docker.pkg.dev && \
    # docker run --gpus all europe-west9-docker.pkg.dev/algorithmic-quartet/training-pipelines/pokemon-trainer:latest
    # """
    studio.run(f"export WANDB_KEY={os.environ.get('WANDB_KEY')}")
    studio.run(f"export GC_BUCKET_KEY={os.environ.get('GC_BUCKET_KEY')}")
    studio.run(
        "cat ~/keys/ar-read-only.json | docker login -u _json_key_base64 --password-stdin https://europe-west9-docker.pkg.dev"
    )
    studio.run(
        "docker run -i -e WANDB_KEY -e GC_BUCKET_KEY europe-west9-docker.pkg.dev/algorithmic-quartet/training-pipelines/pokemon-trainer:latest"
    )
    # jobs_plugin.run(cmd, name="Train model", machine=Machine.CPU)  # type: ignore

    studio.stop()
