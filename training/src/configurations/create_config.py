import argparse

from .Configuration import Configuration
from .DevConfig import DevConfig
from .TrainConfig import TrainConfig


def create_config_from_arguments() -> Configuration:
    parser = argparse.ArgumentParser(
        prog="Pokemon Training Loop",
        description="Trains a model to create new images.",
    )
    parser.add_argument("-t", "--train", action="store_true")
    args = parser.parse_args()
    if args.train:
        return TrainConfig()

    return DevConfig()
