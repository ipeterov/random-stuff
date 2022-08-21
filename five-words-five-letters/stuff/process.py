import json
import string
from collections import Counter


words = set()
with open("wordle-answers-alphabetical.txt", "r") as input:
    for line in input:
        word = line.strip().lower()

        if len(word) != 5:
            continue

        if len(set(word)) != len(word):
            continue

        if any(letter not in string.ascii_letters for letter in word):
            continue

        words.add(word)


by_letters = {}
for word in words:
    key = "".join(sorted(set(word)))
    by_letters[key] = word


letter_counter = Counter()
for word in by_letters.values():
    letter_counter.update(word)


def word_cost(word):
    return sum(letter_counter[letter] for letter in word)


words = sorted(words, key=word_cost)


out = {
    "words": words,
    "letter_counter": letter_counter,
}
with open("data.json", "w") as f:
    json.dump(out, f)
