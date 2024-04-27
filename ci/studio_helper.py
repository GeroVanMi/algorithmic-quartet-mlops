from lightning_sdk import Machine, Studio


def create_studio() -> Studio:
    return Studio(
        "lab-5-image-generation",
        org="CVDL",
        teamspace="group 03",
    )
