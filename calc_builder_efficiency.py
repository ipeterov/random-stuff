import math
import json


WORK = 'work'
CARRY = 'carry'
MOVE = 'move'

COSTS = {
	WORK: 100,
	CARRY: 50,
	MOVE: 50,
}

DISTANCE = 20
WORK_PER_TICK = 5  # 1 for upgrading, 5 for building, 2 for harvesting


def extend_parts(parts):
	assert type(parts) == dict

	extended = []
	for k, v in parts.items():
		extended.extend([k] * v)

	return extended


def repr_parts(parts):
	return ', '.join(f"{k}: {v}" for k, v in parts.items())


def calc_info(parts, verbose=True):
	cycle_time = 0

	# Add trip time
	move_count = parts[MOVE]
	non_move_count = sum(parts.values()) - move_count
	ticks_per_move = math.ceil(non_move_count / (move_count * 2))
	# We assume all movement is on roads
	round_trip_time = ticks_per_move * DISTANCE * 2
	cycle_time += round_trip_time

	# Add work time
	carry_count = parts[CARRY]
	cycle_energy = carry_count * 50
	work_count = parts[WORK]
	working_time = math.ceil(cycle_energy / (WORK_PER_TICK * work_count))
	cycle_time += working_time

	# Calculate energy cost
	cost = sum(COSTS[p] for p in parts)

	# Calculate work per cost
	cycles_per_life = math.floor(1500 / cycle_time)
	total_energy = cycle_energy * cycles_per_life
	energy_per_cost = total_energy / cost

	energy_per_tick = cycle_energy / cycle_time

	if verbose:
		print(f'Cost: {cost}, parts: ({repr_parts(parts)})')
		print(f'Energy delivered for energy spent: {energy_per_cost}')
		print(f'Cycle time: {cycle_time}, (t{round_trip_time} + w{working_time})')
		print(f'Energy per tick: {energy_per_tick}')

	return energy_per_cost


# MAX_ENERGIES = [
# 	300,
# 	550,
# 	800,
# 	1300,
# 	1800,
# 	2300,
# 	5300,
# 	12300,
# ]
MAX_ENERGIES = range(300, 12350, 50)


max_epc = 0
best_parts = None

energy_to_body = {}

for max_energy in MAX_ENERGIES:
	max_move_parts = math.floor((max_energy - 150) / 50)
	for move_parts in range(1, max_move_parts + 1):
		energy_after_move = max_energy - (move_parts * 50)
		max_work_parts = math.floor((energy_after_move - 50) / 100)
		for work_parts in range(1, max_work_parts + 1):
			energy_after_work = energy_after_move - (work_parts * 100)
			parts = {
				MOVE: move_parts,
				WORK: work_parts,
				CARRY: math.floor(energy_after_work / 50)
			}

			epc = calc_info(parts, verbose=False)

			if epc > max_epc:
				max_epc = epc
				best_parts = parts.copy()

	print(
		f'Energy: {max_energy}, '
		f'max EPC: {max_epc}, '
		f'best parts: {repr_parts(best_parts)}'
	)

	energy_to_body[max_energy] = extend_parts(best_parts)

print(json.dumps(energy_to_body))