import os

from lightning_sdk import Studio


def create_studio() -> Studio:
    """
    Creates a lightning AI studio.
    This does not start the studio automatically!
    """
    # TODO: Implement error handling if the variables are not set
    #       With a nice message telling the user what is wrong.
    return Studio(
        os.environ["LIGHTNING_STUDIO"],
        org=os.environ["LIGHTNING_ORGANIZATION"],
        teamspace=os.environ["LIGHTNING_TEAMSPACE"],
    )
