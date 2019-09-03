from autocompletion import add_words_to_base

words = open('zdb-win.txt')
words_list = []

for line in words:
    word = line.split()
    word = {'l' : word[0], 'q' : word[1]}
    words_list.append(word)

add_words_to_base(words_list)
