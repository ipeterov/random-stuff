from anagram import *
a = wordbase()
words = open('words.txt', 'r')
for word in words:
    word = word.strip('\n')
    a.add_word(word)
a.dump_base()
