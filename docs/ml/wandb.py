import random

import docs.ml.wandb as wandb

# Logging into wandb. WANDB_API_KEY env var must be set.
wandb.login()

project_name = 'pytorch-intro'
run_name = 'first-experiment' # If not set, it will be randomly assigned
run_notes = 'Commit message for the run'
config = {
    'epochs': 10,
    'batch_size': 128,
    'lr': 1e-3,
    'dropout': random.uniform(0.01, 0.8),
}

# Creating a wandb run
# A run is the core element of wandb, used to track metrics, create logs, ...
# config var captures any hyperparameters or configurations associated with this specific run
run = wandb.init(project=project_name, name=run_name, notes=run_notes, config=config)

# Config can be accessed from wandb.config

# This simple block simulates a training loop logging metrics
epochs = config['epochs']
offset = random.random() / 5
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset

    metrics = {
        'train/epoch': epoch + 1,
        'train/acc': acc,
        'train/loss': loss,
    }

    # Log metrics for this run in wandb
    # You can also log images, 3d objects, audio, video or even 3d molecules (any data)
    wandb.log(metrics)

# Logging summary metrics
# These differ from .log bc .log saves values for future plotting, whereas .summary displays in the table
wandb.summary['test_acc'] = 0.8

# Finish run
wandb.finish()
