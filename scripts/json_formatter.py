#!/usr/bin/env python3
"""
Validate and pretty-print JSON files.

Usage:
    # Pretty-print a JSON file
    python scripts/json_formatter.py --input raw.json --output pretty.json

    # Validate a JSON file without writing output
    python scripts/json_formatter.py -i raw.json
"""

import argparse
import json
from pathlib import Path
import sys

def format_json(input_file: Path, output_file: Path = None):
    if not input_file.exists():
        print(f"Error: {input_file} does not exist.")
        return False

    try:
        data = json.loads(input_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"JSON is invalid: {e}")
        return False

    if output_file:
        output_file.write_text(json.dumps(data, indent=4, sort_keys=True), encoding="utf-8")
        print(f"Formatted JSON saved to {output_file}")
    else:
        print(json.dumps(data, indent=4, sort_keys=True))

    return True

def main():
    parser = argparse.ArgumentParser(description="Validate and pretty-print JSON files")
    parser.add_argument('--input', '-i', type=Path, required=True, help="Input JSON file path")
    parser.add_argument('--output', '-o', type=Path, help="Output file path (optional)")
    args = parser.parse_args()

    success = format_json(args.input, args.output)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
