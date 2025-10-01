import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAPI_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

with open('fishwish-words.json', 'r') as f:
    word_sets = json.load(f)

clue_sets = []

for i, word_set in enumerate(word_sets):
    print(f"Processing set {i+1}/{len(word_sets)}: {word_set}")

    words_str = ", ".join(word_set)
    prompt = f'Create a set of crossword clues for the following 8 words: {words_str}. Make the clues each under 12 words, clever, and varied in difficulty and style. Do not make them a simple definition, they should be more clever than that. Don\'t make them too easy, so don\'t try to give multiple hints in the clue. Return the response as a JSON array of arrays, where each inner array contains [clue, word]. For example: [["clue1", "word1"], ["clue2", "word2"], ...]'

    response = client.chat.completions.create(
        model="openai/gpt-5-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    content = response.choices[0].message.content

    if "```json" in content:
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()
    elif "```" in content:
        json_start = content.find("```") + 3
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()

    clues = json.loads(content)
    clue_sets.append(clues)

with open('fishwish-clues.json', 'w') as f:
    json.dump(clue_sets, f, indent=2)

print(f"Successfully generated clues for {len(clue_sets)} sets")
