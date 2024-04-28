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

    print("Pulling newest code from git.")
    cmd = f"cd algorithmic-quartet-mlops && git pull"
    jobs_plugin.run(cmd, name="Pulling the newest code", machine=Machine.CPU)  # type: ignore
