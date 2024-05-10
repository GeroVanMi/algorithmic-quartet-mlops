import wandb
from src.Configuration import Configuration


def download_pipeline_files(config: Configuration):
    """
    Initalizes a W&B run and downloads the pipeline files (including the model) from the W&B artifact registry.
    """
    run = wandb.init()

    if run is None:
        raise RuntimeError("Couldn't initalize W&B!")

    artifact = run.use_artifact(config.artifact_name, type="model")
    artifact.download(root=config.output_dir)
    origin_run = artifact.logged_by()
    run.finish()

    return origin_run.id
