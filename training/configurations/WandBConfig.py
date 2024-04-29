import wandb
import yaml


class WandB:
    def __init__(self, project_name: str, entity: str, mode="training", config=None):
        """
        Initializes the W&B configuration based on the selected mode (training, development, production).

        Args:
        project_name (str): Name of the project.
        entity (str): Entity under which the project is registered.
        mode (str): Operation mode, one of 'training', 'development', 'production'.
        config (dict, optional): Configuration dictionary for W&B initialization.
        """
        self.project_name = project_name
        self.entity = entity
        self.mode = mode
        self.config = config if config is not None else {}
        self.run = None

    def create_run(self, experiment_name=None):
        """
        Starts a new W&B run with the specified experiment name and configuration. Adjusts name based on mode.

        Args:
        experiment_name (str, optional): Name of the experiment to be logged.

        Returns:
        wandb.sdk.wandb_run.Run: The W&B run object.
        """
        # Append mode to experiment name if provided
        if experiment_name:
            experiment_name = f"{self.mode.upper()}_{experiment_name}"
        else:
            experiment_name = self.mode.upper()

        self.run = wandb.init(
            project=self.project_name,
            entity=self.entity,
            config=self.config,
            name=experiment_name,
        )
        return self.run

    def log(self, metrics):
        """
        Logs metrics to the current W&B run if it is active. Behavior might differ based on the mode.

        Args:
        metrics (dict): Dictionary of metrics to log.
        """
        if self.run:
            if self.mode == "production":
                # Log only key production metrics
                filtered_metrics = {
                    k: v for k, v in metrics.items() if k in ["throughput", "latency"]
                }
                self.run.log(filtered_metrics)
            else:
                self.run.log(metrics)

    def log_image(self, image, caption):
        """
        Logs an image with a caption to the current W&B run if it is active. Disabled in production mode.

        Args:
        image: Image data.
        caption (str): Caption for the image.
        """
        if self.run and self.mode != "production":
            self.run.log({"image": [wandb.Image(image, caption=caption)]})

    def finish_run(self):
        """
        Finishes the active W&B run.
        """
        if self.run:
            self.run.finish()

    @staticmethod
    def create_sweep(sweep_config, project_name, entity):
        """
        Creates a sweep configuration and initializes a sweep.

        Args:
        sweep_config (dict): Configuration dictionary for the sweep.
        project_name (str): Project name for the sweep.
        entity (str): Entity under which the project is registered.

        Returns:
        str: Sweep ID returned by W&B.
        """
        sweep_id = wandb.sweep(sweep_config, project=project_name, entity=entity)
        return sweep_id

    @staticmethod
    def agent(sweep_id, function):
        """
        Starts an agent for a specific sweep ID and a given function to execute.

        Args:
        sweep_id (str): The sweep ID to run the agent on.
        function (callable): The function to execute for each sweep run.
        """
        wandb.agent(sweep_id, function)


def start_sweep(project_name, entity, config_file):
    """
    Loads a sweep configuration from a YAML file, creates a W&B manager instance, and starts a sweep.

    Args:
    project_name (str): Name of the W&B project.
    entity (str): Entity under which the project is registered.
    config_file (str): Path to the YAML configuration file.

    Returns:
    str: Sweep ID returned by W&B.
    """
    # load YAML-Datei
    with open(config_file, "r") as file:
        sweep_config = yaml.safe_load(file)

    # initialise W&B Manager
    wandb_manager = WandB(project_name, entity)

    # create Sweep and return ID
    sweep_id = wandb_manager.create_sweep(sweep_config)
    return sweep_id


# TODO: Discribe how to add the following code to the training script
# TODO: Define the parameters for the sweep
