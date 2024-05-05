import os

import torch
from configurations.Configuration import Configuration
from diffusers.utils.pil_utils import make_image_grid


def evaluate(config: Configuration, epoch, pipeline):
    # Sample some images from random noise (this is the backward diffusion process).
    # The default pipeline output type is `List[PIL.Image]`
    images = pipeline(
        batch_size=config.eval_batch_size,
        generator=torch.manual_seed(config.seed),
        num_inference_steps=config.number_of_noise_steps,  # TODO: This needs to be set via the config and synced with the training equivalent
    ).images

    # Make a grid out of the images
    # TODO: The rows and cols should be set via config as well
    image_grid = make_image_grid(images, rows=4, cols=4)

    # Save the images
    test_dir = os.path.join(config.output_dir, "samples")
    os.makedirs(test_dir, exist_ok=True)
    image_grid.save(f"{test_dir}/{epoch:04d}.png")
