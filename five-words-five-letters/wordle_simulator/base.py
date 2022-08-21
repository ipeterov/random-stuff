import os


class WordleInfo:
    EXACT = "🟩"
    MISPLACED = "🟨"
    MISS = "⬛"
    # EXACT = "G"
    # MISPLACED = "Y"
    # MISS = "-"

    def __init__(self) -> None:
        print(f"Initializing {self}")

        self.all_words = []

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "data/wordle-answers-alphabetical.txt")

        with open(filename, "r") as input:
            for line in input:
                self.all_words.append(line.strip())

    def __str__(self) -> str:
        return self.__class__.__name__


class BasePlayer(WordleInfo):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.all_words = self.sorted_words()

    def sorted_words(self):
        raise NotImplementedError()

    def reset(self):
        self.guessed_words = set()
        self.guesses = []

    def consider_response(self, guess: str, response: str):
        self.guessed_words.add(guess)
        self.guesses.append([guess, response])

    def match_pattern(self, word, guess, answer):
        required = [g for g, a in zip(guess, answer) if a == self.MISPLACED]
        if not all(letter in word for letter in required):
            return False

        excluded = [g for g, a in zip(guess, answer) if a == self.MISS]
        if any(letter in word for letter in excluded):
            return False

        for w, g, a in zip(word, guess, answer):
            if a == self.MISPLACED and w == g:
                return False

            if a == self.EXACT and w != g:
                return False

        return True

    def get_suitable(self):
        suitable = [
            word
            for word in self.all_words
            if all(
                self.match_pattern(word, guess, answer)
                for guess, answer in self.guesses
            )
        ]
        return [word for word in suitable if word not in self.guessed_words]

    def make_guess(self):
        suitable = self.get_suitable()
        return suitable[0]

    def interactive(self):
        while True:
            guess = self.make_guess()
            print(f"Next word is {guess}")
            response = input("Enter response: ").upper()
            if response == self.EXACT * 5:
                print("Congrats")
                break
            self.consider_response(guess, response)
