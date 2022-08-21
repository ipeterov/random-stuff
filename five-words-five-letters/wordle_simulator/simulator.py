import random
import time
from collections import Counter

from base import WordleInfo


class Simulation(WordleInfo):
    MAX_GUESSES = 6

    def give_response(self, guess):
        response = ""
        for g, a in zip(guess, self.answer):
            if g == a:
                response += self.EXACT
            elif g in self.answer:
                response += self.MISPLACED
            else:
                response += self.MISS
        return response

    def run(self, player, answer=None):
        player.reset()

        if answer is None:
            self.answer = random.choice(self.all_words)
        else:
            self.answer = answer

        for current_move in range(self.MAX_GUESSES):
            guess = player.make_guess()
            response = self.give_response(guess)
            if response == self.EXACT * 5:
                return current_move
            player.consider_response(guess, response)

        print("lost", answer)

        return self.MAX_GUESSES

    def run_for_all_words(self, player):
        self.stats = Counter()

        self.words_done_so_far = 0
        t = time.time()
        for answer in self.all_words:
            result = self.run(player, answer=answer)
            player.reset()
            self.stats[result] += 1
            self.words_done_so_far += 1
            if self.words_done_so_far % 100 == 0:
                print(".", end="", flush=True)
        total_time = time.time() - t

        print(f"\nResults of {player}, time {total_time:.2f}s")
        self.print_stats()

    def print_stats(self):
        mean = sum(k * v for k, v in self.stats.items()) / sum(
            v for v in self.stats.values()
        )
        print(f"Mean {mean}")
        for key in sorted(self.stats.keys()):
            frequency_dots = "*" * (self.stats[key] // 7)
            frequency = (self.stats[key] / self.words_done_so_far) * 100
            print(f"{key}\t{frequency:.2f}%\t{frequency_dots}")
