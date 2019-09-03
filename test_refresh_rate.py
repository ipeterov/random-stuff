import random
import subprocess
import time


CMD = 'xrandr --output DVI-D-0 --mode 1920x1080 --rate {rate}'
COUNT = 10
RATES = [60, 120]


def get_counts(total_rates, count):
    base = count / total_rates
    remainder = count - base * total_rates
    counts = [base] * total_rates
    for i in range(remainder):
        counts[i] += 1
    random.shuffle(counts)
    return counts


def run_test():
    rates = []
    for rate, count in zip(RATES, get_counts(len(RATES), COUNT)):
        for i in range(count):
            rates.append(rate)
    random.shuffle(rates)

    raw_input('Starting test, press anything to continue...')
    guesses = []
    for rate in rates:
        print 'Changing in 3 seconds...'
        time.sleep(3)
        subprocess.check_output(CMD.format(rate=rate), shell=True)
        guesses.append(int(raw_input('Current rate: ')))

    matches = [guesses[i] == rates[i] for i in range(len(rates))]
    right_count = len([match for match in matches if match])

    print 'Actual rates:', rates
    print 'Guesses:     ', guesses
    print '{} guessed right out of {}'.format(right_count, len(rates))

    return rates


if __name__ == '__main__':
    run_test()
