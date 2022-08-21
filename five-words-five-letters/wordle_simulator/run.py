from simulator import Simulation
from word_score import WordScorePlayer
from alphabet import AlphabetPlayer
from similarity import SimilarityPlayer
from magic_words import MagicWordsPlayer

fucker_words = [
    "boxer",
    "brave",
    "catch",
    "crook",
    "found",
    "frank",
    "frown",
    "fully",
    "grave",
    "graze",
    "hatch",
    "jaunt",
    "joker",
    "jolly",
    "mover",
    "shave",
    "taste",
    "tatty",
    "taunt",
    "tight",
    "waver",
    "witty",
    "wound",
    "fewer",
]

if __name__ == "__main__":
    sim = Simulation()

    # for word in fucker_words:
    print(sim.run(WordScorePlayer(), "tight"))

    # sim.run_for_all_words(WordScorePlayer())

    # WordScorePlayer().interactive()
