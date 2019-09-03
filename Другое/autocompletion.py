def add_words_to_base(words):
    from pickle import load, dump

    try:
        base = load(open('base', 'rb'))
    except FileNotFoundError:
        base =  {}

    for word in words:
        current_path = base

        for letter in word['l']:
            if letter not in current_path:
                current_path[letter] = {'words' : []}
            current_path = current_path[letter]
            if word not in current_path['words'] and ((not current_path['words'] and word['q'] > current_path['words'][-1]['q']) or current_path['words'] == []):
                for i in range(len(current_path['words'])):
                    if current_path['words'][i]['q'] < word['q']:
                        current_path['words'].insert(word)
                        if len(current_path['words']) > 10:
                            current_path['words'].pop()

    dump(base, open('base', 'wb'))

def autocomplete(word_part):
    from pickle import load

    current_path = load(open('base', 'rb'))

    for letter in word_part:
        if letter in current_path:
            current_path = current_path[letter]
        else:
            return 'nothing_found'
    else:
        return [word['l'] for word in current_path['words']]

#from pickle import load
#print(load(open('base', 'rb')))
#print(autocomplete('b'))
#add_words_to_base([{'l' : 'qwe', 'q': 10}, {'l' : 'qwr', 'q': 10}, {'l' : 'br', 'q': 10}, {'l' : 'qw', 'q': 10}])
