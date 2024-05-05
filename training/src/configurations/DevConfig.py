from dataclasses import dataclass

from .Configuration import Configuration


@dataclass
class DevConfig(Configuration):
    train_batch_size = 1
    eval_batch_size = 16  # how many images to sample during evaluation (at least 16)
    num_epochs = 1
    num_images = 6
