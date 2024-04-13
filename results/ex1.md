# Project Documentation: Causal Variational Autoencoder (CausalVAE)

## Introduction
The Causal Variational Autoencoder (CausalVAE) project is a machine learning project that focuses on training a VAE model on video datasets. This project provides a set of configurable parameters through the `TrainingArguments` class for training the model with various options to customize the training process.

## Code Summary
The codebase consists of the following documented functions:
1. `TrainingArguments`: A class that defines configurable training parameters.
2. `set_seed(seed)`: Function to set a seed for random number generation for reproducibility.
3. `load_callbacks_and_logger(args)`: Function to initialize and return callback objects and a logger for model training.
4. `train(args)`: Function to train the CausalVAE model on a video dataset using the specified configuration and parameters.

Now, let's dive deeper into each of the documented functions and their usage.

## TrainingArguments
The `TrainingArguments` class defines various configurable parameters for training the model. These parameters include `exp_name`, `batch_size`, `precision`, `max_steps`, `save_steps`, `output_dir`, and more. Each parameter has a default value and a help string explaining its purpose.

Example Usage:
```python
args = TrainingArguments()
print(args.output_dir)
```

## set_seed(seed)
The `set_seed(seed)` function sets the seed for random number generation in PyTorch, NumPy, and Python's built-in `random` module. This ensures reproducibility of results in machine learning applications.

Usage Example:
```python
set_seed(42)
```

## load_callbacks_and_logger(args)
The `load_callbacks_and_logger` function initializes and returns callback and logger objects for model training. It includes a `ModelCheckpoint` callback for saving model checkpoints and a `LearningRateMonitor` for monitoring learning rates, along with a `WandbLogger` for logging experiment metrics to the Weights & Biases platform.

Usage Example:
```python
callbacks, logger = load_callbacks_and_logger(args)
model_checkpoint_callback, lr_monitor = callbacks
```

## train(args)
The `train(args)` function is used to train a Causal Variational Autoencoder model on a given video dataset. It includes setting a seed, loading the model, dataset, callbacks, and logger, configuring the Trainer, fitting the model to the training data, and saving the trained model in the Huggingface format.

Usage Example:
```python
args = {
    "video_path": "path/to/video/dataset",
    "batch_size": 8,
    "devices": [0],
    "n_nodes": 1,
    ...
}

train(args)
```

This documentation provides a comprehensive guide on the provided functions and their usage within the CausalVAE project.
