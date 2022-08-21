from base import BasePlayer


class SimilarityPlayer(BasePlayer):
    GREEN_SCORE = 1
    YELLOW_SCORE = 0.5

    def sorted_words(self):
        similarity_record = {}
        for word in self.all_words:
            similarity_sum = 0
            for other_word in self.all_words:
                similarity_sum += self.similarity(word, other_word)
            similarity_record[word] = similarity_sum / len(self.all_words)
        return sorted(self.all_words, key=lambda w: similarity_record[w])

    def similarity(self, word1, word2):
        score = 0
        for l1, l2 in zip(word1, word2):
            if l1 == l2:
                score += self.GREEN_SCORE
            elif l1 in word2:
                score += self.YELLOW_SCORE
        return score
