from lightning_sdk import Machine, Status
from studio_helper import create_studio

if __name__ == "__main__":
    # start studio
    studio = create_studio()

    # if studio.status != "Running": # TODO: Uncomment this line
    print(studio.status)
    studio.start()
    print(studio.status)

    # use the jobs plugin
    jobs_plugin = studio.installed_plugins["jobs"]

    cmd = f"cd algorithmic-quartet-mlops && git pull"
    jobs_plugin.run(cmd, name="Pulling the newest code", machine=Machine.CPU)  # type: ignore

    studio.stop()
