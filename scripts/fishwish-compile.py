import json
import random
from pathlib import Path

script_dir = Path(__file__).parent
clues_file = script_dir / "fishwish-clues.json"
output_file = script_dir.parent / "static" / "fishwish-games.json"

with open(clues_file, 'r') as f:
    clue_sets = json.load(f)

games = []

for clue_set in clue_sets:
    if len(clue_set) != 8:
        raise ValueError(f"Expected 8 clues in set, got {len(clue_set)}")

    pairs = []
    for i in range(0, 8, 2):
        left_item = clue_set[i]
        right_item = clue_set[i + 1]
        pairs.append((left_item, right_item))

    left = [pair[0] for pair in pairs]

    right = [pair[1] for pair in pairs]

    match_order = list(range(4))

    combined = list(zip(left, match_order))
    while match_order == [0, 1, 2, 3]:
        random.shuffle(combined)
        left, match_order = zip(*combined)
        left = list(left)
        match_order = list(match_order)

    game = {
        "left": left,
        "right": right,
        "match_order": match_order
    }

    games.append(game)

with open(output_file, 'w') as f:
    json.dump(games, f, indent=4)


