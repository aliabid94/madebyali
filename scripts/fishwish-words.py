import pronouncing
from collections import defaultdict
import random

SET_COUNT = 10
SET_SIZE = 8

import nltk
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download('brown')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

brown_words = [word.lower() for word in brown.words() if word.isalpha()]

root_words = []
for word in brown_words:
    if not word.isalpha() or word.lower() != word:
        continue
    root = lemmatizer.lemmatize(word, pos='v')
    root = lemmatizer.lemmatize(root, pos='n')
    if len(root) < 3:
        continue
    if not pronouncing.phones_for_word(root):
        continue
    root_words.append(root)

word_freq = Counter(root_words)
common_words = [word for word, _ in word_freq.most_common(3000)]


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

rhyme_sets = []
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
        print(selected_words)
        accept = input("Accept? (y/n): ")
        if accept.lower() != 'y':
            continue
        for word in selected_words:
            rhyme_set.append(word)
            words.remove(word)
        last_phonemes_used.add(last_phoneme)
    rhyme_sets.append(rhyme_set)
    print(", ".join(rhyme_set))

import json
with open("fishwish-words.json", "w") as f:
    json.dump(rhyme_sets, f, indent=2)