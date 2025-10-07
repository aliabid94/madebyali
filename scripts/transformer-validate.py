import json
from pathlib import Path

# Load the valid words set
script_dir = Path(__file__).parent
with open(script_dir.parent / "static" / "all-words.json", 'r') as f:
    common_words = set(json.load(f))

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

    for candidate in common_words:
        if candidate != word and ''.join(sorted(candidate)) == sorted_word:
            results.append(candidate)

    return results

def is_valid_transformation(word1, word2):
    """Check if word2 is a valid transformation of word1."""
    word1 = word1.lower()
    word2 = word2.lower()

    # Check all transformation types
    if word2 in find_removals(word1):
        return True, 'removal'
    if word2 in find_insertions(word1):
        return True, 'insertion'
    if word2 in find_replacements(word1):
        return True, 'replacement'
    if word2 in find_anagrams(word1):
        return True, 'anagram'

    return False, None

def validate_game(game, game_index):
    """Validate a single game chain."""
    errors = []

    if len(game) < 2:
        errors.append(f"Game {game_index}: Chain too short (needs at least 2 words)")
        return errors

    for i in range(len(game)):
        word = game[i].lower()

        # Check if word is in valid word list
        if word not in common_words:
            errors.append(f"Game {game_index}, word {i} ('{game[i]}'): Not in valid word list")

        # Check transformation to next word
        if i < len(game) - 1:
            next_word = game[i + 1].lower()
            is_valid, transform_type = is_valid_transformation(word, next_word)

            if not is_valid:
                errors.append(f"Game {game_index}, transformation {i}→{i+1} ('{game[i]}' → '{game[i+1]}'): Invalid transformation")
            # else:
            #     print(f"Game {game_index}, transformation {i}→{i+1}: {game[i]} → {game[i+1]} ({transform_type})")

    return errors

def main():
    # Load games
    games_path = script_dir.parent / "static" / "transformer-games.json"
    with open(games_path, 'r') as f:
        games = json.load(f)

    print(f"Validating {len(games)} games...")
    print()

    all_errors = []
    valid_count = 0

    for i, game in enumerate(games):
        errors = validate_game(game, i)
        if errors:
            all_errors.extend(errors)
        else:
            valid_count += 1

    # Print results
    if all_errors:
        print("VALIDATION ERRORS:")
        print("=" * 60)
        for error in all_errors:
            print(f"  {error}")
        print()

    print("=" * 60)
    print(f"Valid games: {valid_count}/{len(games)}")
    print(f"Invalid games: {len(games) - valid_count}/{len(games)}")

    if all_errors:
        print(f"\nTotal errors: {len(all_errors)}")
        exit(1)
    else:
        print("\n✓ All games are valid!")
        exit(0)

if __name__ == "__main__":
    main()
