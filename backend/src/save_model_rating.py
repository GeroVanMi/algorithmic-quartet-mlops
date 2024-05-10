import wandb
from src.Configuration import Configuration


def wandb_rate_model(run_id: str, rating: int, config: Configuration):
    run = wandb.init(
        project=config.wandb_project,
        entity=config.wandb_entity,
        id=run_id,
        resume="must",
    )
    run.log({"user_rating": rating})
    run.finish()
