#!/usr/bin/env python3
"""
Summarize a text file: word count, sentence count, paragraph count, most frequent words.

Usage:
    # Summarize a text file
    python scripts/text_summarizer.py --input sample.txt

    # Show top 5 most frequent words
    python scripts/text_summarizer.py -i sample.txt --top 5
"""

import argparse
from pathlib import Path
from collections import Counter
import string
import sys

def summarize_text(file_path: Path, top_n: int = 5):
    if not file_path.exists():
        print(f"Error: {file_path} does not exist.")
        return False

    text = file_path.read_text(encoding="utf-8")

    # Paragraphs
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    num_paragraphs = len(paragraphs)

    # Sentences (split by . ! ?)
    sentences = [s for s in text.replace("\n", " ").split('.') if s.strip()]
    num_sentences = len(sentences)

    # Words
    words = text.translate(str.maketrans('', '', string.punctuation)).split()
    num_words = len(words)
    avg_word_length = sum(len(w) for w in words) / max(num_words, 1)

    # Most frequent words
    word_counts = Counter([w.lower() for w in words])
    most_common = word_counts.most_common(top_n)

    # Display summary
    print(f"File: {file_path}")
    print(f"Paragraphs: {num_paragraphs}")
    print(f"Sentences: {num_sentences}")
    print(f"Words: {num_words}")
    print(f"Average word length: {avg_word_length:.2f}")
    print(f"Top {top_n} most frequent words:")
    for word, count in most_common:
        print(f"  {word}: {count}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Summarize a text file")
    parser.add_argument('--input', '-i', type=Path, required=True, help="Path to text file")
    parser.add_argument('--top', '-t', type=int, default=5, help="Top N frequent words")
    args = parser.parse_args()

    success = summarize_text(args.input, args.top)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
