from lightning_sdk import Machine
from studio_helper import create_studio


def switch_machine():
    studio = create_studio()
    studio.switch_machine(Machine.T4)


if __name__ == "__main__":
    switch_machine()
