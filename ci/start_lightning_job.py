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

    BASE_PATH = "/teamspace/studios/this_studio/algorithmic-quartet-mlops"
    # Update the code to the latest commit
    studio.run(f"git -C {BASE_PATH} pull")

    # Update the dependencies
    studio.run(f"pip install -r {BASE_PATH}/training/requirements.txt")

    # Setup the cloud storage bucket
    studio.run(f"bash {BASE_PATH}/training/setup_gc.sh")

    # Run the pipeline on the CPU once, to make sure that there are no errors
    output, exit_code = studio.run(f"python {BASE_PATH}/training/pipeline.py")

    # If there are errors, raise an exception and stop the execution!
    if exit_code != 0:
        print(output)
        raise RuntimeError("Training pipeline did not run successfully!")

    # Use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    # Start the training pipeline on a GPU job
    cmd = f"python {BASE_PATH}/training/pipeline.py --training"
    jobs_plugin.run(cmd, name="Train model", machine=Machine.T4)  # type: ignore
