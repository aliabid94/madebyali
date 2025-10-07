import pronouncing
from collections import defaultdict
import random

SET_COUNT = 10
SET_SIZE = 8

import nltk
from pathlib import Path
import json

nltk.download('wordnet')

script_dir = Path(__file__).parent
words_file = script_dir / "fishwish-words.json"

existing_words = []
rhyme_sets = []
if words_file.exists():
    with open(words_file, 'r') as f:
        for rhyme_set in json.load(f):
            rhyme_sets.append(rhyme_set)
            existing_words.extend(rhyme_set)

# Load common words from generated JSON
with open(script_dir.parent / "static" / "common-words.json", 'r') as f:
    all_common_words = json.load(f)

# Filter to words with pronunciations and limit to 3000
common_words = []
for word in all_common_words:
    if len(word) < 3:
        continue
    if not pronouncing.phones_for_word(word):
        continue
    common_words.append(word)
    if len(common_words) >= 3000:
        break

def get_rhyming_phoneme(word):
    pronunciations = pronouncing.phones_for_word(word)
    if not pronunciations:
        return None
    return pronouncing.rhyming_part(pronunciations[0])


rhyme_dict = defaultdict(list)

for word in common_words:
    phoneme = get_rhyming_phoneme(word)
    if phoneme:
        rhyme_dict[phoneme].append(word)

rhyme_dict = {k: v for k, v in rhyme_dict.items() if len(v) > 1}

for i in range(SET_COUNT):
    rhyme_set = []
    last_phonemes_used = set()
    while len(rhyme_set) < SET_SIZE:
        phoneme = random.choice(list(rhyme_dict.keys()))
        if len(rhyme_dict[phoneme]) < 2:
            del rhyme_dict[phoneme]
            continue
        last_phoneme = phoneme.split(" ")[-1]
        if last_phoneme in last_phonemes_used:
            continue
        words = rhyme_dict[phoneme]
        selected_words = random.sample(words, 2)
        if any(word in existing_words for word in selected_words):
            continue
        print(selected_words)
        accept = input("Accept? (y/n): ")
        if accept.lower() != 'y':
            continue
        for word in selected_words:
            rhyme_set.append(word)
            words.remove(word)
        last_phonemes_used.add(last_phoneme)
    rhyme_sets.append(rhyme_set)
    with open(words_file, 'w') as f:
        json.dump(rhyme_sets, f, indent=2)
    print(", ".join(rhyme_set))

