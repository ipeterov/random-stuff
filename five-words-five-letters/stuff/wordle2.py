import json


with open("data.json") as f:
    data = json.load(f)
words = data["words"]
words.reverse()


def match_pattern(word, guess, answer):
    """
    - is grey
    * is yellow
    + is green
    """
    required = [g for g, a in zip(guess, answer) if a == "*"]
    if not all(letter in word for letter in required):
        return False

    excluded = [g for g, a in zip(guess, answer) if a == "-"]
    if any(letter in word for letter in excluded):
        return False

    for w, g, a in zip(word, guess, answer):
        if a != "+":
            continue
        if w != g:
            return False

    return True


def suggest_words(guesses: list[list[str]]):
    suitable = [
        word
        for word in words
        if all(match_pattern(word, guess, answer) for guess, answer in guesses)
    ]
    print(suitable[:10])


guesses = [
    ["slate", "--**-"],
    ["ratio", "*+*--"],
]

suggest_words(guesses)
