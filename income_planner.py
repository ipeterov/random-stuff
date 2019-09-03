import random


state_chains = [
    {'probability': 1, 'values': [0]}
]

moves = [(1000, 0.5), (300, 0.9), (400, 0.7)]

per_move_decrease = 1


for balance_inrease, increase_probability in moves:
    new_state_chains = []
    for state_chain in state_chains:
        last_value = state_chain['values'][-1]

        # success
        success_chain = {
            'probability': state_chain['probability'] * increase_probability,
            'values': state_chain['values'] + [last_value + balance_inrease - per_move_decrease],
        }

        # failure
        failure_chain = {
            'probability': state_chain['probability'] * (1 - increase_probability),
            'values': state_chain['values'] + [last_value - per_move_decrease],
        }

        new_state_chains.extend((success_chain, failure_chain))

    state_chains = new_state_chains

print sum([chain['probability'] for chain in state_chains if all(value >= 0 for value in chain['values'])])

