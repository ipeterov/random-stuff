import pickle

def char_structure(word):
    chars = {}
    for char in word:
        if char not in chars:
            chars[char] = 1
        else:
            chars[char] += 1
    chars = list(chars.items())
    return chars

class wordbase:
    def __init__(self):
        self.lengths = {}

    def dump_base(self, filename='anagram_wordbase'):
        with open(filename, 'wb') as outfile:
            pickle.dump(self.lengths, outfile)

    def load_base(self, filename='anagram_wordbase'):
        with open(filename, 'rb') as infile:
            self.lengths = pickle.load(infile)

    def add_word(self,word):
        if len(word) not in self.lengths:
            self.lengths[len(word)] = {}
        for char in char_structure(word):
            if char in self.lengths[len(word)]:
                self.lengths[len(word)][char].add(word)
            else:
                self.lengths[len(word)][char] = set([word])

    def find_words(self, anagram):
        if len(anagram) in self.lengths:
            chars = char_structure(anagram)
            wordsets = []
            for char in chars:
                if char in self.lengths[len(anagram)]:
                    wordsets.append(self.lengths[len(anagram)][char])
                else:
                    return False
            for wordset in wordsets[1:]:
                wordsets[0].intersection_update(wordset)
            return list(wordsets[0])
        else:
            return False
