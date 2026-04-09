"""Fine-tune Gemma 4 E4B on Modal with A100-40GB GPU.

Runs Unsloth QLoRA fine-tuning, saves LoRA adapters + GGUF export to a Modal volume.

Usage:
    modal run deploy/modal_finetune.py        # Run fine-tuning
    modal run deploy/modal_finetune.py::download_results  # Download GGUF to local
"""

import modal

MINUTES = 60

# Volume to persist fine-tuned model outputs
output_vol = modal.Volume.from_name("navigator-finetune-output", create_if_missing=True)

finetune_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install(
        "unsloth @ git+https://github.com/unslothai/unsloth.git",
        "trl",
        "peft",
        "accelerate",
        "bitsandbytes",
        "datasets",
        "torch",
        "torchvision",
        "sentencepiece",
        "protobuf",
        "rich",
		"unsloth_zoo @ git+https://github.com/unslothai/unsloth_zoo.git",
    )
    .pip_install(
        # Install after unsloth so this overrides its transformers pin.
        # Gemma 4 (gemma4 arch) requires unreleased transformers from git.
        "git+https://github.com/huggingface/transformers.git",
    )
    .add_local_file("data/training/generated.jsonl", remote_path="/data/generated.jsonl", copy=True)
)

app = modal.App("navigator-finetune", image=finetune_image)


@app.function(
    gpu="A100-40GB",
    timeout=60 * MINUTES,
    volumes={"/output": output_vol},
    secrets=[modal.Secret.from_name("huggingface")],
)
def finetune():
    """Run QLoRA fine-tuning with Unsloth on A100."""
    import json
    import torch
    from unsloth import FastLanguageModel
    from trl import SFTTrainer, SFTConfig
    from datasets import Dataset

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

    # --- Load model ---
    MAX_SEQ_LENGTH = 2048  # A100 has plenty of room

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/gemma-4-E4B-it",
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=True,
        dtype=None,  # Let Unsloth auto-select — explicit float16 causes OOM via upcasting
    )

    print(f"Model loaded: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        lora_alpha=16,  # alpha/r = 1.0 (proven stable for Gemma 4)
        lora_dropout=0.0,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        bias="none",
        use_gradient_checkpointing="unsloth",  # ~30% VRAM savings
        random_state=42,
    )
    model.print_trainable_parameters()

    # --- Load training data ---
    records = []
    with open("/data/generated.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    formatted_texts = []
    for ex in records:
        text = tokenizer.apply_chat_template(
            ex["messages"], tokenize=False, add_generation_prompt=False
        )
        formatted_texts.append(text)

    dataset = Dataset.from_dict({"text": formatted_texts})
    print(f"Training examples: {len(dataset)}")

    # --- Train ---
    # Use SFTConfig (not TrainingArguments) — includes SFT-specific params.
    # Don't set fp16/bf16 — Unsloth handles Gemma 4 precision internally.
    training_args = SFTConfig(
        output_dir="/output/checkpoints",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        logging_steps=5,
        save_steps=50,
        save_total_limit=2,
        optim="adamw_8bit",
        seed=42,
        report_to="none",
        dataset_num_proc=2,
        max_seq_length=MAX_SEQ_LENGTH,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        args=training_args,
    )

    print("Starting training...")
    result = trainer.train()
    metrics = result.metrics
    print(f"Training complete! Loss: {metrics.get('train_loss', 'N/A'):.4f}")
    print(f"Runtime: {metrics.get('train_runtime', 0):.1f}s")

    # --- Save LoRA adapters ---
    model.save_pretrained("/output/lora")
    tokenizer.save_pretrained("/output/lora")
    print("LoRA adapters saved to /output/lora")

    # --- Export GGUF ---
    print("Exporting GGUF (q4_k_m)...")
    model.save_pretrained_gguf(
        "/output/gguf",
        tokenizer,
        quantization_method="q4_k_m",
    )
    print("GGUF exported to /output/gguf")

    # --- Create Ollama Modelfile ---
    import os
    gguf_files = [f for f in os.listdir("/output/gguf") if f.endswith(".gguf")]
    gguf_filename = gguf_files[0] if gguf_files else "model.gguf"

    system_prompt = (
        "You are NorthStar Navigator, a plain-language government benefits navigator for Minnesota. "
        "You help people understand which government assistance programs they may "
        "be eligible for based on their situation. Be warm, clear, and actionable. "
        "Always cite specific eligibility thresholds and application portals. "
        'Never say someone "qualifies" — say "may be eligible." '
        "End every response with a disclaimer that this is informational, not legal advice."
    )
    modelfile = f"""FROM ./{gguf_filename}
PARAMETER temperature 1.0
PARAMETER top_p 0.95
PARAMETER num_ctx 2048
SYSTEM "{system_prompt}"
"""
    with open("/output/gguf/Modelfile", "w") as f:
        f.write(modelfile)
    print("Modelfile written.")

    # --- Test inference ---
    print("\n--- Test Inference ---")
    FastLanguageModel.for_inference(model)
    test_messages = [{"role": "user", "content":
        "I'm a single mom with two kids ages 3 and 7. I just lost my job "
        "last week and I live in Hennepin County. What help is available?"}]

    inputs = tokenizer.apply_chat_template(
        test_messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs, max_new_tokens=512,
            temperature=1.0, top_p=0.95, do_sample=True,
        )
    response = tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)
    print(response[:500])

    # Commit volume
    output_vol.commit()

    # List outputs
    for root, dirs, files in os.walk("/output/gguf"):
        for f in files:
            path = os.path.join(root, f)
            size = os.path.getsize(path) / 1024 / 1024
            print(f"  {path} ({size:.1f} MB)")

    print("\nDone! Run `modal run deploy/modal_finetune.py::download_results` to download.")


@app.function(
    volumes={"/output": output_vol},
    timeout=30 * MINUTES,
)
def download_results():
    """List files in the output volume."""
    import os
    print("Files in output volume:")
    for root, dirs, files in os.walk("/output"):
        for f in files:
            path = os.path.join(root, f)
            size = os.path.getsize(path) / 1024 / 1024
            print(f"  {path} ({size:.1f} MB)")


@app.local_entrypoint()
def main():
    finetune.remote()
