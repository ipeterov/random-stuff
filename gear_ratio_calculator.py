import itertools
import functools
from fractions import Fraction

MAX_GEAR_TRAIN_LENGTH = 5

gear_costs = {
    (12, 20): 1,
    (8, 24): 1,
    (12, 28): 1,
    (20, 28): 1,
    (12, 36): 1,
    (8, 40): 1,
    (28, 36): 1,
    (24, 40): 1,
    (16, 20): 10,
    (12, 24): 10,
    (8, 28): 10,
    (20, 24): 10,
    (16, 28): 10,
    (8, 36): 10,
    (24, 28): 10,
    (20, 36): 10,
    (16, 40): 10,
    (28, 40): 10,
    (12, 40): 10,
}

for (gear1, gear2), cost in list(gear_costs.items()):
    gear_costs[(gear2, gear1)] = cost


def format_combination(combination: list[tuple[int]]):
    return " > ".join(f"{n}/{d}" for n, d in combination)


def suggest_gears(required_ratio: str):
    answers = []

    try:
        for combination_length in range(1, MAX_GEAR_TRAIN_LENGTH):
            for combination in itertools.combinations_with_replacement(
                gear_costs.keys(),
                combination_length,
            ):
                combination = tuple(sorted(combination))
                result = functools.reduce(lambda x, y: x * Fraction(*y), combination, 1)
                if result == Fraction(required_ratio):
                    cost = sum(gear_costs[gear] for gear in combination)
                    answers.append((cost, combination))
    except KeyboardInterrupt:
        print("\nStopping early...")

    answers.sort()

    for cost, combination in answers:
        print(f"cost: {cost}, {format_combination(combination)}")


if __name__ == "__main__":
    suggest_gears("1/12")
