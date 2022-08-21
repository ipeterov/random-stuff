import json


with open("data.json") as f:
    data = json.load(f)
words = data["words"]
words.reverse()


def match_pattern(word, pattern):
    for w, p in zip(word, pattern):
        if p == "*":
            continue
        if w != p:
            return False
    return True


def suggest_word(pattern: str, excluded: str, included: str, to_suggest: list[str]):
    to_suggest = [
        word for word in to_suggest if not any(letter in excluded for letter in word)
    ]
    to_suggest = [
        word for word in to_suggest if all(letter in word for letter in included)
    ]
    to_suggest = [word for word in to_suggest if match_pattern(word, pattern)]
    print(to_suggest[:10])


suggest_word("****e", excluded="iatsnopug", included="r", to_suggest=words)
