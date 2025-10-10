import json
import sys
from pathlib import Path


def load_json(filepath: Path) -> list:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def validate_words_schema(words_data: list, filepath: Path) -> bool:
    """Validate the schema of fishwish-words.json."""
    errors = []

    # Check if it's a list
    if not isinstance(words_data, list):
        errors.append(f"Root element must be a list, got {type(words_data).__name__}")
        return errors

    # Check each puzzle set
    for i, puzzle_set in enumerate(words_data):
        if not isinstance(puzzle_set, list):
            errors.append(f"Puzzle set {i} must be a list, got {type(puzzle_set).__name__}")
            continue

        if len(puzzle_set) != 8:
            errors.append(f"Puzzle set {i} must have exactly 8 words, got {len(puzzle_set)}")

        # Check each word
        for j, word in enumerate(puzzle_set):
            if not isinstance(word, str):
                errors.append(f"Puzzle set {i}, word {j} must be a string, got {type(word).__name__}")
            elif not word.strip():
                errors.append(f"Puzzle set {i}, word {j} is empty")

    return errors


def validate_clues_schema(clues_data: list, filepath: Path) -> bool:
    """Validate the schema of fishwish-clues.json."""
    errors = []

    # Check if it's a list
    if not isinstance(clues_data, list):
        errors.append(f"Root element must be a list, got {type(clues_data).__name__}")
        return errors

    # Check each puzzle set
    for i, puzzle_set in enumerate(clues_data):
        if not isinstance(puzzle_set, list):
            errors.append(f"Puzzle set {i} must be a list, got {type(puzzle_set).__name__}")
            continue

        if len(puzzle_set) != 8:
            errors.append(f"Puzzle set {i} must have exactly 8 clue/word pairs, got {len(puzzle_set)}")

        # Check each clue/word pair
        for j, pair in enumerate(puzzle_set):
            if not isinstance(pair, list):
                errors.append(f"Puzzle set {i}, pair {j} must be a list, got {type(pair).__name__}")
                continue

            if len(pair) != 2:
                errors.append(f"Puzzle set {i}, pair {j} must have exactly 2 elements (clue, word), got {len(pair)}")
                continue

            clue, word = pair
            if not isinstance(clue, str):
                errors.append(f"Puzzle set {i}, pair {j}: clue must be a string, got {type(clue).__name__}")
            elif not clue.strip():
                errors.append(f"Puzzle set {i}, pair {j}: clue is empty")

            if not isinstance(word, str):
                errors.append(f"Puzzle set {i}, pair {j}: word must be a string, got {type(word).__name__}")
            elif not word.strip():
                errors.append(f"Puzzle set {i}, pair {j}: word is empty")

    return errors


def validate_consistency(words_data: list, clues_data: list) -> list:
    """Validate that words.json and clues.json are consistent."""
    errors = []

    # Check same number of puzzle sets
    if len(words_data) != len(clues_data):
        errors.append(f"Number of puzzle sets mismatch: words.json has {len(words_data)}, clues.json has {len(clues_data)}")
        return errors

    # Check each puzzle set
    for i in range(len(words_data)):
        if not isinstance(words_data[i], list) or not isinstance(clues_data[i], list):
            continue  # Skip if schema validation already caught this

        words_set = words_data[i]
        clues_set = clues_data[i]

        # Check same number of items
        if len(words_set) != len(clues_set):
            errors.append(f"Puzzle set {i}: word count mismatch - words.json has {len(words_set)}, clues.json has {len(clues_set)}")
            continue

        # Check each word matches
        for j in range(min(len(words_set), len(clues_set))):
            if isinstance(words_set[j], str) and isinstance(clues_set[j], list) and len(clues_set[j]) >= 2:
                word_from_words = words_set[j].strip().lower()
                word_from_clues = clues_set[j][1].strip().lower()

                if word_from_words != word_from_clues:
                    errors.append(f"Puzzle set {i}, position {j}: word mismatch - words.json: '{words_set[j]}', clues.json: '{clues_set[j][1]}'")

    return errors


def main():
    """Main validation function."""
    # Get script directory
    script_dir = Path(__file__).parent

    # File paths
    words_file = script_dir / "fishwish-words.json"
    clues_file = script_dir / "fishwish-clues.json"

    print("🔍 Validating fishwish game data files...\n")

    # Load files
    print(f"📂 Loading {words_file.name}...")
    words_data = load_json(words_file)
    print(f"✅ Loaded {len(words_data)} puzzle sets\n")

    print(f"📂 Loading {clues_file.name}...")
    clues_data = load_json(clues_file)
    print(f"✅ Loaded {len(clues_data)} puzzle sets\n")

    # Validate schemas
    all_errors = []

    print("🔎 Validating words.json schema...")
    words_errors = validate_words_schema(words_data, words_file)
    if words_errors:
        all_errors.extend([f"[words.json] {e}" for e in words_errors])
        print(f"❌ Found {len(words_errors)} error(s)")
    else:
        print("✅ Schema valid")
    print()

    print("🔎 Validating clues.json schema...")
    clues_errors = validate_clues_schema(clues_data, clues_file)
    if clues_errors:
        all_errors.extend([f"[clues.json] {e}" for e in clues_errors])
        print(f"❌ Found {len(clues_errors)} error(s)")
    else:
        print("✅ Schema valid")
    print()

    print("🔎 Validating consistency between files...")
    consistency_errors = validate_consistency(words_data, clues_data)
    if consistency_errors:
        all_errors.extend([f"[consistency] {e}" for e in consistency_errors])
        print(f"❌ Found {len(consistency_errors)} error(s)")
    else:
        print("✅ Files are consistent")
    print()

    # Print results
    if all_errors:
        print("=" * 60)
        print(f"❌ VALIDATION FAILED: {len(all_errors)} error(s) found\n")
        for error in all_errors:
            print(f"  • {error}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("=" * 60)
        print("✅ VALIDATION PASSED: All checks successful!")
        print(f"   - {len(words_data)} puzzle sets validated")
        print(f"   - {len(words_data) * 8} words verified")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
