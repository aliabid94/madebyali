#!/usr/bin/env python3
"""
Generate common-words.json and all-words.json for word games.

common-words.json: 20k most common words from NLTK Brown corpus
all-words.json: 50k most common from Brown + 50k from Reuters + all words length > 5 from comprehensive list
"""

import json
import nltk
import inflect
from collections import Counter
from pathlib import Path

# Download required NLTK data
try:
    nltk.data.find('corpora/brown')
except LookupError:
    print("Downloading NLTK Brown corpus...")
    nltk.download('brown')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK WordNet...")
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/reuters')
except LookupError:
    print("Downloading NLTK Reuters corpus...")
    nltk.download('reuters')


def get_brown_words():
    """Get word frequency from Brown corpus."""
    print("Loading Brown corpus...")
    brown_words = [word.lower() for word in nltk.corpus.brown.words() if word.isalpha()]
    return Counter(brown_words)


def get_reuters_words():
    """Get word frequency from Reuters corpus."""
    print("Loading Reuters corpus...")
    reuters_words = [word.lower() for word in nltk.corpus.reuters.words() if word.isalpha()]
    return Counter(reuters_words)


def get_comprehensive_words():
    """Get comprehensive English word list with plurals."""
    print("Loading comprehensive word list...")
    base_words = set(word.lower() for word in nltk.corpus.words.words() if word.isalpha())

    print("Generating plurals...")
    p = inflect.engine()
    words_with_plurals = set(base_words)

    for word in base_words:
        # Generate plural form
        plural = p.plural(word)
        if plural and plural.isalpha():
            words_with_plurals.add(plural.lower())

    print(f"Added {len(words_with_plurals) - len(base_words)} plural forms")
    return words_with_plurals


def main():
    # Get Brown corpus word frequencies
    brown_freq = get_brown_words()

    # Get most common words from Brown corpus
    most_common_brown = [word for word, _ in brown_freq.most_common()]

    # Generate common-words.json (20k most common)
    common_words = most_common_brown[:20000]
    print(f"Generated {len(common_words)} common words")

    # Get Reuters corpus word frequencies
    reuters_freq = get_reuters_words()
    most_common_reuters = [word for word, _ in reuters_freq.most_common()]

    # Generate all-words.json (50k most common from Brown + 20k from Reuters + long words from comprehensive list)
    all_words_set = set(most_common_brown[:50000])
    all_words_set.update(set(most_common_reuters[:20000]))

    # Add all words length > 5 from comprehensive list
    comprehensive = get_comprehensive_words()
    long_words = {word for word in comprehensive if len(word) > 4 and len(word) < 12}
    all_words_set.update(long_words)

    # Convert to sorted list
    all_words = sorted(list(all_words_set))
    print(f"Generated {len(all_words)} total words")

    # Write to files
    static_dir = Path(__file__).parent.parent / "static"
    static_dir.mkdir(exist_ok=True)

    common_path = static_dir / "common-words.json"
    all_path = static_dir / "all-words.json"

    print(f"Writing to {common_path}...")
    with open(common_path, 'w') as f:
        json.dump(common_words, f, indent=2)

    print(f"Writing to {all_path}...")
    with open(all_path, 'w') as f:
        json.dump(all_words, f, indent=2)

    print("Done!")
    print(f"  - common-words.json: {len(common_words)} words")
    print(f"  - all-words.json: {len(all_words)} words")


if __name__ == "__main__":
    main()
