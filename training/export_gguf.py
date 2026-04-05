"""Export Unsloth fine-tuned model to GGUF format for Ollama.

Usage:
    python training/export_gguf.py --model training/output/final --output training/output/gguf

After export, create an Ollama model:
    ollama create navigator-e4b -f training/output/gguf/Modelfile
"""

import argparse
from pathlib import Path

from unsloth import FastLanguageModel


def main():
    parser = argparse.ArgumentParser(description="Export fine-tuned model to GGUF")
    parser.add_argument("--model", required=True, help="Path to fine-tuned model")
    parser.add_argument("--output", default="training/output/gguf", help="Output directory")
    parser.add_argument("--quant", default="q4_k_m", help="Quantization method")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the fine-tuned model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=2048,
        load_in_4bit=True,
    )

    # Export to GGUF
    model.save_pretrained_gguf(
        str(output_dir),
        tokenizer,
        quantization_method=args.quant,
    )

    # Create Ollama Modelfile
    modelfile_content = f"""FROM {output_dir / f'unsloth.{args.quant.upper()}.gguf'}
PARAMETER temperature 1.0
PARAMETER top_p 0.95
PARAMETER top_k 64
SYSTEM "You are a plain-language government benefits navigator."
"""
    modelfile_path = output_dir / "Modelfile"
    modelfile_path.write_text(modelfile_content)

    print(f"GGUF exported to {output_dir}")
    print(f"Modelfile written to {modelfile_path}")
    print(f"\nTo create Ollama model, run:")
    print(f"  ollama create navigator-e4b -f {modelfile_path}")


if __name__ == "__main__":
    main()
