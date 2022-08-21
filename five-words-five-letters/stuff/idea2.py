import json
import time


N_WORDS = 5

with open("data.json") as f:
    data = json.load(f)

four_letter = 0


cache = {}


def search_words(
    words: list,
    new_letters: set,
    current_letters: set,
    current_found_words: list,
    start: bool = False,
):
    if len(current_found_words) == 4:
        global four_letter
        four_letter += 1

    if len(current_found_words) >= N_WORDS:
        print(current_found_words)
        return

    key = "".join(sorted(current_letters))
    if key in cache:
        acceptable_words = cache[key]
    else:
        acceptable_words = [word for word in words if new_letters.isdisjoint(word)]
        cache[key] = acceptable_words

    if not acceptable_words:
        return

    for word in acceptable_words:
        new_letters = set(word)
        letters = current_letters | new_letters
        found_words = current_found_words + [word]

        t = time.time()
        result = search_words(
            acceptable_words,
            new_letters,
            letters,
            found_words,
        )

        if start:
            timing = time.time() - t
            print(word, timing, int(four_letter / timing))
            four_letter = 0


start_words = data["words"]
print(search_words(start_words, set(), set(), [], start=True))
