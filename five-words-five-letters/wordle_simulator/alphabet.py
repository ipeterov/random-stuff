from base import BasePlayer


class AlphabetPlayer(BasePlayer):
    def sorted_words(self):
        return sorted(self.all_words)
