import pickle
import string

name = input('Введите название файла (без расширения): ') + '.txt'
text = open(name).read()

words = text.split()

for i in range(len(words)):
    words[i] = words[i].lower().strip(''',.:;!?()'"_-@©''')

words = set(words)
badchars = ['--']
goodchars = string.ascii_lowercase + '-'

for word in words.copy():
    remove = 0
    if not 3 < len(word) < 15:
        remove = 1

    for symbol in badchars:
        if symbol in word:
            remove = 1

    for symbol in word:
        if symbol not in goodchars:
            remove = 1

    if remove:
        words.remove(word)
try:
    old_words = pickle.load(open('words', 'rb'))
    words = words | old_words
except:
    pass

pickle.dump(words, open('words', 'wb'))

words = list(words)
words.sort()
new_file = open('words.txt', 'w')
for word in words:
    new_file.write(word + '\n')
