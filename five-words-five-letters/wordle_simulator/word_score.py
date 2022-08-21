from collections import Counter

from base import BasePlayer


class WordScorePlayer(BasePlayer):
    KNOWN_DISCOUNT = 0.5

    def __init__(self) -> None:
        self.known_letters = set()
        super().__init__()
        # self.magic_words = ["flame", "shunt", "brick", "podgy"]
        self.magic_words = []

    def sorted_words(self):
        self.letter_counter = Counter()
        for word in self.all_words:
            self.letter_counter.update(word)
        return sorted(self.all_words, key=self.word_score, reverse=True)

    def consider_response(self, guess: str, response: str):
        print(guess, response)
        return super().consider_response(guess, response)

    def word_score(self, word):
        score = 0
        for letter in set(word):
            if letter in self.known_letters:
                score += self.letter_counter[letter] * self.KNOWN_DISCOUNT
            score += self.letter_counter[letter]
        return score

    def make_guess(self):
        if self.magic_words:
            return self.magic_words.pop(0)
        self.all_words = self.sorted_words()
        suitable = self.get_suitable()
        print("considering", suitable[:10])
        guess = suitable[0]
        self.known_letters.update(guess)
        return guess
