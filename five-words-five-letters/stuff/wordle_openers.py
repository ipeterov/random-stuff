from audioop import reverse
import json


with open("data.json") as f:
    data = json.load(f)
words = data["words"]
words.reverse()


def similarity(word1, word2):
    score = 0
    for l1, l2 in zip(word1, word2):
        if l1 == l2:
            score += 1
        elif l1 in word2:
            score += 0.2
    return score


similarity_record = []
for word in words:
    similarity_sum = 0
    for other_word in words:
        similarity_sum += similarity(word, other_word)
    similarity_record[word] = similarity_sum / len(words)


words.sort(key=lambda w: similarity_record[w], reverse=True)
