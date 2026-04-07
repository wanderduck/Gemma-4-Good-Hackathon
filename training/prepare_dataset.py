"""Merge and validate training data for Navigator fine-tuning.

Combines all JSONL files in data/training/ into a single dataset,
validates format, deduplicates, and reports statistics.

Usage:
    python training/prepare_dataset.py
    python training/prepare_dataset.py --output data/training/final.jsonl
"""

import argparse
import json
import hashlib
from pathlib import Path
from collections import Counter


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file, skip malformed lines."""
    records = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  WARNING: {path.name} line {i}: {e}")
    return records


def validate_example(ex: dict, idx: int) -> list[str]:
    """Validate a single training example. Returns list of issues."""
    issues = []
    if "messages" not in ex:
        issues.append(f"Example {idx}: missing 'messages' key")
        return issues

    msgs = ex["messages"]
    if not isinstance(msgs, list) or len(msgs) < 2:
        issues.append(f"Example {idx}: need at least 2 messages (system+user or user+assistant)")
        return issues

    roles = [m.get("role") for m in msgs]

    if roles[0] not in ("system", "user"):
        issues.append(f"Example {idx}: first message should be system or user, got '{roles[0]}'")

    if "assistant" not in roles:
        issues.append(f"Example {idx}: no assistant message found")

    for j, m in enumerate(msgs):
        if not m.get("content", "").strip():
            issues.append(f"Example {idx}, message {j}: empty content")

    # Check assistant response length
    for m in msgs:
        if m.get("role") == "assistant":
            words = len(m["content"].split())
            if words < 50:
                issues.append(f"Example {idx}: assistant response too short ({words} words)")
            if words > 1500:
                issues.append(f"Example {idx}: assistant response very long ({words} words)")

    return issues


def content_hash(ex: dict) -> str:
    """Hash based on user message content for dedup."""
    user_msgs = [m["content"] for m in ex.get("messages", []) if m.get("role") == "user"]
    text = " ".join(user_msgs)
    return hashlib.md5(text.encode()).hexdigest()


def analyze_dataset(examples: list[dict]) -> None:
    """Print dataset statistics."""
    print(f"\n{'='*60}")
    print(f"Dataset Statistics")
    print(f"{'='*60}")
    print(f"Total examples: {len(examples)}")

    # Language detection
    langs = Counter()
    for ex in examples:
        for m in ex.get("messages", []):
            if m.get("role") == "user":
                content = m["content"].lower()
                if any(w in content for w in ["soy", "necesito", "tengo", "trabajo", "hijos", "ayuda"]):
                    langs["Spanish"] += 1
                elif any(w in content for w in ["kuv", "nyob", "pab", "muaj"]):
                    langs["Hmong"] += 1
                elif any(w in content for w in ["waxaan", "lacag", "qoys"]):
                    langs["Somali"] += 1
                else:
                    langs["English"] += 1

    print(f"\nLanguage distribution:")
    for lang, count in langs.most_common():
        print(f"  {lang}: {count} ({count/len(examples)*100:.0f}%)")

    # Response length stats
    assistant_lengths = []
    for ex in examples:
        for m in ex.get("messages", []):
            if m.get("role") == "assistant":
                assistant_lengths.append(len(m["content"].split()))

    if assistant_lengths:
        print(f"\nAssistant response length (words):")
        print(f"  Min: {min(assistant_lengths)}")
        print(f"  Max: {max(assistant_lengths)}")
        print(f"  Avg: {sum(assistant_lengths)/len(assistant_lengths):.0f}")

    # Multi-turn detection
    multi_turn = sum(1 for ex in examples if sum(1 for m in ex.get("messages", []) if m.get("role") == "user") > 1)
    print(f"\nMulti-turn examples: {multi_turn}")

    # Programs mentioned
    programs = Counter()
    program_keywords = {
        "SNAP": ["snap", "food support", "food stamp"],
        "MFIP": ["mfip", "minnesota family investment"],
        "Medical Assistance": ["medical assistance", "medicaid"],
        "MinnesotaCare": ["minnesotacare"],
        "CCAP": ["ccap", "child care assistance"],
        "Energy Assistance": ["energy assistance", "heating", "liheap"],
        "Emergency Assistance": ["emergency assistance"],
        "GA": ["general assistance"],
        "UI": ["unemployment insurance", "unemployment benefits"],
        "WIC": ["wic"],
        "RCA": ["refugee cash assistance", "rca"],
        "SSI/MSA": ["ssi", "msa", "supplemental"],
    }
    for ex in examples:
        for m in ex.get("messages", []):
            if m.get("role") == "assistant":
                content = m["content"].lower()
                for prog, keywords in program_keywords.items():
                    if any(kw in content for kw in keywords):
                        programs[prog] += 1

    print(f"\nProgram coverage:")
    for prog, count in programs.most_common():
        print(f"  {prog}: mentioned in {count} examples")

    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Prepare Navigator training dataset")
    parser.add_argument("--output", default="data/training/final.jsonl", help="Output path")
    parser.add_argument("--data-dir", default="data/training", help="Directory with JSONL files")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_path = Path(args.output)

    # Collect all JSONL files
    jsonl_files = sorted(data_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"No JSONL files found in {data_dir}")
        return

    print(f"Found {len(jsonl_files)} JSONL files:")
    all_examples = []
    for f in jsonl_files:
        if f.name == output_path.name:
            continue  # skip the output file itself
        records = load_jsonl(f)
        print(f"  {f.name}: {len(records)} examples")
        all_examples.extend(records)

    print(f"\nTotal loaded: {len(all_examples)}")

    # Validate
    all_issues = []
    for i, ex in enumerate(all_examples):
        issues = validate_example(ex, i)
        all_issues.extend(issues)

    if all_issues:
        print(f"\nValidation issues ({len(all_issues)}):")
        for issue in all_issues[:20]:
            print(f"  - {issue}")
        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more")
    else:
        print("\nAll examples passed validation.")

    # Deduplicate
    seen = set()
    unique = []
    dupes = 0
    for ex in all_examples:
        h = content_hash(ex)
        if h not in seen:
            seen.add(h)
            unique.append(ex)
        else:
            dupes += 1

    if dupes:
        print(f"\nRemoved {dupes} duplicates.")
    print(f"Unique examples: {len(unique)}")

    # Analyze
    analyze_dataset(unique)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        for ex in unique:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"\nWritten to {output_path}")


if __name__ == "__main__":
    main()
