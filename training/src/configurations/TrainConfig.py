from dataclasses import dataclass

from .Configuration import Configuration


@dataclass
class TrainConfig(Configuration):
    train_batch_size = 96
    eval_batch_size = 8
    num_epochs = 60
    num_images = 7351
