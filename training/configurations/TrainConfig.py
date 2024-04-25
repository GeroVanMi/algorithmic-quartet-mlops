from dataclasses import dataclass

from .Configuration import Configuration


@dataclass
class TrainConfig(Configuration):
    train_batch_size = 32
    eval_batch_size = 16  # how many images to sample during evaluation (at least 16)
    num_epochs = 20