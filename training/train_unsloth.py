"""Fine-tune Gemma 4 E4B with Unsloth + QLoRA.

Run on Kaggle T4 (16 GB) or local RTX 2080 Ti (11 GB).

Usage:
    python training/train_unsloth.py --dataset data/training/combined.jsonl

Dataset format (JSONL, one JSON object per line):
    {"messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]}

See docs/research/toolchain_reference_guide.md for detailed Unsloth docs.
"""

import argparse
import json
from pathlib import Path

from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import Dataset


def load_dataset(path: str) -> Dataset:
    """Load JSONL dataset into HuggingFace Dataset format."""
    records = []
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    return Dataset.from_list(records)


def format_chat(example: dict) -> dict:
    """Format a chat example for training."""
    messages = example["messages"]
    # Unsloth handles chat template formatting internally
    return {"messages": messages}


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Gemma 4 E4B with Unsloth")
    parser.add_argument("--dataset", required=True, help="Path to JSONL training data")
    parser.add_argument("--output", default="training/output", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--max-seq-length", type=int, default=2048)
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load model with Unsloth optimizations
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="google/gemma-4-E4B-it",
        max_seq_length=args.max_seq_length,
        load_in_4bit=True,
        dtype=None,  # auto-detect
    )

    # Add LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_rank,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=args.lora_rank * 2,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    # Load and prepare dataset
    dataset = load_dataset(args.dataset)
    dataset = dataset.map(format_chat)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        fp16=False,
        bf16=True,
        optim="adamw_8bit",
        seed=42,
        report_to="none",
    )

    # Create trainer
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_args,
        max_seq_length=args.max_seq_length,
    )

    # Train
    print(f"Training on {len(dataset)} examples for {args.epochs} epochs...")
    trainer.train()

    # Save
    model.save_pretrained(str(output_dir / "final"))
    tokenizer.save_pretrained(str(output_dir / "final"))
    print(f"Model saved to {output_dir / 'final'}")


if __name__ == "__main__":
    main()
