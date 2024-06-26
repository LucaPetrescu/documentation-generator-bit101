from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

ex1 = """
class TrainingArguments:
    exp_name: str = field(
        default="causalvae", metadata={"help": "The name of the experiment."}
    )
    batch_size: int = field(
        default=1, metadata={"help": "The number of samples per training iteration."}
    )
    precision: str = field(
        default="bf16",
        metadata={"help": "The precision type used for training."},
    )
    max_steps: int = field(
        default=100000,
        metadata={"help": "The maximum number of steps for the training process."},
    )
    save_steps: int = field(
        default=2000,
        metadata={"help": "The interval at which to save the model during training."},
    )
    output_dir: str = field(
        default="results/causalvae",
        metadata={"help": "The directory where training results are saved."},
    )
    video_path: str = field(
        default="/remote-home1/dataset/data_split_tt",
        metadata={"help": "The path where the video data is stored."},
    )
    video_num_frames: int = field(
        default=17, metadata={"help": "The number of frames per video."}
    )
    sample_rate: int = field(
        default=1,
        metadata={
            "help": "The sampling interval."
        },
    )
    dynamic_sample: bool = field(
        default=False, metadata={"help": "Whether to use dynamic sampling."}
    )
    model_config: str = field(
        default="scripts/causalvae/288.yaml",
        metadata={"help": "The path to the model configuration file."},
    )
    n_nodes: int = field(
        default=1, metadata={"help": "The number of nodes used for training."}
    )
    devices: int = field(
        default=8, metadata={"help": "The number of devices used for training."}
    )
    resolution: int = field(
        default=256, metadata={"help": "The resolution of the videos."}
    )
    num_workers: int = field(
        default=8,
        metadata={"help": "The number of subprocesses used for data handling."},
    )
    resume_from_checkpoint: str = field(
        default=None, metadata={"help": "Resume training from a specified checkpoint."}
    )
    load_from_checkpoint: str = field(
        default=None, metadata={"help": "Load the model from a specified checkpoint."}
    )
"""
ex2 = """
def set_seed(seed=1006):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
"""

ex3 = """
def load_callbacks_and_logger(args):
    checkpoint_callback = ModelCheckpoint(
        dirpath=args.output_dir,
        filename="model-{epoch:02d}-{step}",
        every_n_train_steps=args.save_steps,
        save_top_k=-1,
        save_on_train_epoch_end=False,
    )
    lr_monitor = LearningRateMonitor(logging_interval="step")
    logger = WandbLogger(name=args.exp_name, log_model=False)
    return [checkpoint_callback, lr_monitor], logger
"""

ex4 = """
def train(args):
    set_seed()
    # Load Config
    model = CausalVAEModel()
    if args.load_from_checkpoint is not None:
        model = CausalVAEModel.from_pretrained(args.load_from_checkpoint)
    else:
        model = CausalVAEModel.from_config(args.model_config)

    if (dist.is_initialized() and dist.get_rank() == 0) or not dist.is_initialized():
        print(model)

    # Load Dataset
    dataset = VideoDataset(
        args.video_path,
        sequence_length=args.video_num_frames,
        resolution=args.resolution,
        sample_rate=args.sample_rate,
        dynamic_sample=args.dynamic_sample,
    )
    train_loader = DataLoader(
        dataset,
        shuffle=True,
        num_workers=args.num_workers,
        batch_size=args.batch_size,
        pin_memory=True,
    )
    # Load Callbacks and Logger
    callbacks, logger = load_callbacks_and_logger(args)
    # Load Trainer
    trainer = pl.Trainer(
        accelerator="cuda",
        devices=args.devices,
        num_nodes=args.n_nodes,
        callbacks=callbacks,
        logger=logger,
        log_every_n_steps=5,
        precision=args.precision,
        max_steps=args.max_steps,
        strategy="ddp_find_unused_parameters_true",
    )
    trainer_kwargs = {}
    if args.resume_from_checkpoint:
        trainer_kwargs["ckpt_path"] = args.resume_from_checkpoint

    trainer.fit(model, train_loader, **trainer_kwargs)
    # Save Huggingface Model
    model.save_pretrained(os.path.join(args.output_dir, "hf"))
"""

example_md = """
## load_callbacks_and_logger
```python
def load_callbacks_and_logger(args):
    checkpoint_callback = ModelCheckpoint(
        dirpath=args.output_dir,
        filename="model-{epoch:02d}-{step}",
        every_n_train_steps=args.save_steps,
        save_top_k=-1,
        save_weights_only=True,
        save_on_train_epoch_end=False,
    )
    lr_monitor = LearningRateMonitor(logging_interval="step")
    logger = WandbLogger(name=args.exp_name, log_model=False)
    return [checkpoint_callback, lr_monitor], logger
```

**Improvements:**
- Change `save_top_k=-1` to `save_weights_only=True` in the `ModelCheckpoint` to only save the model weights.
- None Found

**Errors:**
- None Found

**Vulnerabilities:**
- None Found

"""

client = OpenAI()

def upgrade_function(func:str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "text" },
    temperature=0.0,
    messages=[
        {"role": "system", "content": "You are a developer that has to improve a given function or class and find possible errors or exploits. Rewrite the given code and return a markdown with the code and 3 lists: improvements, errors, vulnerabilities. The title is the function or class name If there any of the lists is empty, display the text None Found. Do not add or consider imports an error or improvement."},
        {"role": "system", "content": "Use the following structure" + example_md},
        {"role": "user", "content": f"Fix this function: {func}"}
    ]
    )
    return response.choices[0].message.content


if __name__=="__main__":
    examples = [ex1, ex2, ex3, ex4]

    for ex in examples:
        print(upgrade_function(ex))