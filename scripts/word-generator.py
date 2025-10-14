#!/usr/bin/env python3
"""
Generate common-words.json, all-words.json, and all-words-8-letter-max.json for word games.

common-words.json: 20k most common words from NLTK Brown corpus
all-words.json: Official Scrabble word list from norvig.com
all-words-8-letter-max.json: Scrabble words filtered to 8 letters or less
"""

import json
import nltk
import urllib.request
from collections import Counter
from pathlib import Path

# Download required NLTK data
try:
    nltk.data.find('corpora/brown')
except LookupError:
    print("Downloading NLTK Brown corpus...")
    nltk.download('brown')


def get_brown_words():
    """Get word frequency from Brown corpus."""
    print("Loading Brown corpus...")
    brown_words = [word.lower() for word in nltk.corpus.brown.words() if word.isalpha()]
    return Counter(brown_words)


def download_scrabble_words():
    """Download official Scrabble word list from norvig.com."""
    url = "https://norvig.com/ngrams/enable1.txt"

    print(f"Downloading word list from {url}...")

    try:
        # Download the word list
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')

        # Split by newlines and filter out empty strings
        words = [word.strip() for word in content.split('\n') if word.strip()]

        print(f"Downloaded {len(words)} words")
        return words

    except Exception as e:
        print(f"Error downloading Scrabble words: {e}")
        return None


def main():
    # Setup output directory
    static_dir = Path(__file__).parent.parent / "static"
    static_dir.mkdir(exist_ok=True)

    # Download Scrabble words (used for all-words.json)
    print("\n=== Downloading Scrabble Words ===")
    all_words = download_scrabble_words()

    if all_words is None:
        print("Failed to download Scrabble words. Exiting.")
        return 1

    # Filter to 8 letters max for all-words-8-letter-max.json
    all_words_8_max = [word for word in all_words if len(word) <= 8]
    print(f"Filtered to {len(all_words_8_max)} words (8 letters max)")

    # Get Brown corpus word frequencies for common-words.json
    print("\n=== Generating Common Words from Brown Corpus ===")
    brown_freq = get_brown_words()
    most_common_brown = [word for word, _ in brown_freq.most_common()]
    common_words = most_common_brown[:20000]
    print(f"Generated {len(common_words)} common words")

    # Write to files
    common_path = static_dir / "common-words.json"
    all_path = static_dir / "all-words.json"
    all_8_max_path = static_dir / "all-words-8-letter-max.json"

    print("\n=== Writing Files ===")
    print(f"Writing to {common_path}...")
    with open(common_path, 'w') as f:
        json.dump(common_words, f, indent=2)

    print(f"Writing to {all_path}...")
    with open(all_path, 'w') as f:
        json.dump(all_words, f, indent=2)

    print(f"Writing to {all_8_max_path}...")
    with open(all_8_max_path, 'w') as f:
        json.dump(all_words_8_max, f, indent=2)

    print("\n=== Summary ===")
    print(f"  - common-words.json: {len(common_words)} words (from NLTK Brown corpus)")
    print(f"  - all-words.json: {len(all_words)} words (from norvig.com Scrabble list)")
    print(f"  - all-words-8-letter-max.json: {len(all_words_8_max)} words (Scrabble list, 8 letters max)")

    return 0


if __name__ == "__main__":
    exit(main())
