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

with open('fishwish-clues.json', 'r') as f:
    clue_sets = json.load(f)

word_sets = word_sets[len(clue_sets):]

for i, word_set in enumerate(word_sets):
    print(f"Processing set {i+1}/{len(word_sets)}: {word_set}")

    clue_set = []
    for word in word_set:
        prompt = f'Create 3 different crossword clues for the word "{word}". Make each clue each under 12 words, clever, and varied in difficulty and style. Do not make them a simple definition, they should be more clever than that. Don\'t make them too easy, so don\'t try to give multiple hints in the clue. Return the response as an array of strings. For example: ["clue1", "clue2", "clue3"].'

        print(f"Generating clues for '{word}' with prompt: {prompt}")
        response = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content = response.choices[0].message.content
        print(f"Raw response for '{word}': {content}")

        if "```json" in content:
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        elif "```" in content:
            json_start = content.find("```") + 3
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()

        clues = [word, json.loads(content)]
        print(f"Generated clues for '{word}': {clues[1]}")
        clue_set.append(clues)
    clue_sets.append(clue_set)

with open('fishwish-clues.json', 'w') as f:
    json.dump(clue_sets, f, indent=2)

print(f"Successfully generated clues for {len(clue_sets)} sets")
