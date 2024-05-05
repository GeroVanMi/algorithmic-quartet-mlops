## Integration in the training script

To integrate the WanDB class into a training script:

`from WanDBConfig import WanDB`
`wandb_manager = WanDB("YourProjectName", "YourEntity", mode='training')`
`wandb_manager.create_run("Training_Experiment")`

`for epoch in range(10):`
    `metrics = {'loss': 0.1 * epoch, 'accuracy': 0.8 + 0.01 * epoch}`
    `wandb_manager.log(metrics)`