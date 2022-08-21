import json

N_WORDS = 4

with open("data.json") as f:
    data = json.load(f)


words = data["words"]
found_words = []
letters = set()

while len(found_words) < N_WORDS:
    for word in words:
        if set(word).intersection(letters):
            continue
        if not found_words:
            print(f"Trying {word}")

        found_words.append(word)
        letters.update(word)
        break
    else:
        found_words = []
        letters = set()
        words = words[1:]

print(found_words)
