from lightning_sdk import Machine, Studio

if __name__ == "__main__":
    # start studio
    s = Studio(
        "lab-5-image-generation",
        org="CVDL",
        teamspace="group 03",
    )
    s.start()

    # use the jobs plugin
    jobs_plugin = s.installed_plugins["jobs"]

    # ----------------------------
    # Configure you own search space in plain Python instead of clunky abstractions
    # ----------------------------
    cmd = f"echo 'Hello World'"
    jobs_plugin.run(cmd, name="sweep", machine=Machine.CPU)
