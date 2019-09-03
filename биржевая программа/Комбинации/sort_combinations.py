def sort_combinations(self_length, after_length):
    from pickle import *
    from lib import *

    sectors = load(open('sectors', 'rb'))

    def make_combinations_and_keysets():
        global good_combinations
        global good_combinations_keys
        global bad_combinations
        global bad_combinations_keys
        good_combinations = []
        good_combinations_keys = []
        bad_combinations = []
        bad_combinations_keys = []
        for sector in sectors:
            good_combinations.append(combinations_dict(sector, self_length, after_length, sectors = 1))
        for combination in good_combinations:
            good_combinations_keys.append(set(combination.keys()))
        for sector in sectors:
            bad_combinations.append(combinations_dict(sector, self_length, after_length, bad_combinations = 1, sectors = 1))
        for combination in bad_combinations:
            bad_combinations_keys.append(set(combination.keys()))

    def make_final_keyset():
        global good_combinations_keys_sum
        global bad_combinations_keys_sum
        good_combinations_keys_sum = good_combinations_keys[0]
        for i in range(1, len(good_combinations_keys)):
            good_combinations_keys_sum = good_combinations_keys_sum | good_combinations_keys[i]
        bad_combinations_keys_sum = bad_combinations_keys[0]
        for i in range(1, len(bad_combinations_keys)):
            bad_combinations_keys_sum = bad_combinations_keys_sum | bad_combinations_keys[i]
        global keyset
        keyset = good_combinations_keys_sum - bad_combinations_keys_sum

    all_combinations = load(open('all_combinations', 'rb'))
    #bad_combinations = load(open('all_combinations', 'rb'))
    #good_combinations = load(open('all_combinations', 'rb'))
    make_combinations_and_keysets()
    make_final_keyset()

    for key in all_combinations.copy():
        if key not in keyset:
            del all_combinations[key]

    #print(good_combinations)
    #for key in good_combinations.copy():
        #if key not in good_combinations_keys_sum:
            #del good_combinations[key]

    #for key in bad_combinations.copy():
        #if key not in bad_combinations_keys_sum:
            #del bad_combinations[key]

    dump(all_combinations, open('sorted_combinations', 'wb'))
    #dump(good_combinations, open('good_combinations', 'wb'))
    #dump(bad_combinations, open('bad_combinations', 'wb'))
