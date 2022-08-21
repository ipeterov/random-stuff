from base import BasePlayer


class MagicWordsPlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__()
        self.magic_words = ["fjord", "gucks", "nymph", "vibex", "waltz"]

    def sorted_words(self):
        return sorted(self.all_words)

    def make_guess(self):
        if self.magic_words:
            return self.magic_words.pop()
        return super().make_guess()
