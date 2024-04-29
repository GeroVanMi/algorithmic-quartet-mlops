from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    # start studio
    studio = create_studio()

    if studio.status != "Status.Running":
        print("Starting studio.")
        studio.start()
    else:
        print("Studio is already running. Not starting it again.")

    # use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    # Update to the newest version & Start the training script
    cmd = f"""
    git -C /teamspace/studios/this_studio/algorithmic-quartet-mlops pull && \
    bash /teamspace/studios/this_studio/algorithmic-quartet-mlops/ci/lightning_run_pipeline.sh
    """
    jobs_plugin.run(cmd, name="Train model", machine=Machine.CPU)  # type: ignore
