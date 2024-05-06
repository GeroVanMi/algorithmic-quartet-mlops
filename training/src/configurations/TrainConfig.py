from dataclasses import dataclass

from .Configuration import Configuration


@dataclass
class TrainConfig(Configuration):
    train_batch_size = 24
    eval_batch_size = 8
    num_epochs = 10
    num_images = 1000
