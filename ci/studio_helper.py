import os

from lightning_sdk import Studio


def create_studio() -> Studio:
    """
    Creates a lightning AI studio.
    This does not start the studio automatically!
    """
    studio = os.environ.get("LIGHTNING_STUDIO")
    org = os.environ.get("LIGHTNING_ORGANIZATION")
    teamspace = os.environ.get("LIGHTNING_TEAMSPACE")

    if studio is None or org is None or teamspace is None:
        raise OSError("Environment variables for lightning are not set!")

    return Studio(
        studio,
        org=org,
        teamspace=teamspace,
    )
