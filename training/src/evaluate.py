import os

import torch
from configurations.Configuration import Configuration


def evaluate(config: Configuration, epoch, pipeline):
    # Sample some images from random noise (this is the backward diffusion process).
    # The default pipeline output type is `List[PIL.Image]`
    images = pipeline(
        batch_size=config.eval_batch_size,
        generator=torch.manual_seed(config.seed),
        num_inference_steps=config.number_of_noise_steps,  # TODO: This needs to be set via the config and synced with the training equivalent
    ).images

    test_dir = os.path.join(config.output_dir, "samples")
    test_dir = os.path.join(test_dir, f"epoch_{epoch}")
    os.makedirs(test_dir, exist_ok=True)

    for index, image in enumerate(images):
        image.save(f"{test_dir}/{index:0>2}.png")
