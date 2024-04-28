from lightning_sdk import Machine
from studio_helper import create_studio

if __name__ == "__main__":
    print("Creating studio instance.")
    # start studio
    studio = create_studio()

    # use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    print("Starting pipeline test.")
    cmd = f"cd algorithmic-quaretet-mlops/training && python pipeline.py"
    jobs_plugin.run(cmd, name="Testing pipeline for errors", machine=Machine.CPU)  # type: ignore
