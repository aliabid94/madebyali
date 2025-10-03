import nltk
from nltk.corpus import brown
from collections import Counter

nltk.download('brown', quiet=True)

brown_words = [word.lower() for word in brown.words() if word.isalpha()]

word_freq = Counter(brown_words)
common_words = set([word for word, _ in word_freq.most_common(50000)])

from pathlib import Path
script_dir = Path(__file__).parent

import json
with open(script_dir.parent / "static" / "transformer-valid-words.json", 'w') as f:
    json.dump(list(common_words), f)

def find_removals(word):
    """Find valid words by removing a single letter."""
    results = []
    for i in range(len(word)):
        new_word = word[:i] + word[i+1:]
        if new_word in common_words and new_word != word:
            results.append(new_word)
    return results

def find_insertions(word):
    """Find valid words by inserting a single letter anywhere."""
    results = []
    for i in range(len(word) + 1):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i:]
            if new_word in common_words and new_word != word:
                results.append(new_word)
    return results

def find_replacements(word):
    """Find valid words by replacing a single letter."""
    results = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i+1:]
            if new_word in common_words and new_word != word:
                results.append(new_word)
    return results

def find_anagrams(word):
    """Find valid words by rearranging the letters."""
    results = []
    sorted_word = ''.join(sorted(word))

    # More efficient: check if any word in the word bank is an anagram
    for candidate in common_words:
        if candidate != word and ''.join(sorted(candidate)) == sorted_word:
            results.append(candidate)

    return results

def explore_word(word, max_depth=8):
    word = word.lower()

    if word not in common_words:
        print(f"Warning: '{word}' is not in the word bank")
        print()

    queue = [(word, [word], {'-': 0, '+': 0, 'r': 0, 'a': 0})]
    visited = {word}

    while queue:
        current, history, types = queue.pop(0)
        depth = len(history)

        if depth >= max_depth:
            continue

        removals = find_removals(current)
        insertions = find_insertions(current)
        replacements = find_replacements(current)
        anagrams = find_anagrams(current)

        transforms = set(removals + insertions + replacements + anagrams)
        transforms = [w for w in transforms if w not in visited]

        for t in transforms:
            ty = dict(types)
            if t in removals:
                ty['-'] += 1
            if t in insertions:
                ty['+'] += 1
            if t in replacements:
                ty['r'] += 1
            if t in anagrams:
                ty['a'] += 1

            print(json.dumps(history + [t]), ty)

            visited.add(t)
            queue.append((t, history + [t], ty))

while True:
    word = input("Word: ").strip()
    explore_word(word)
