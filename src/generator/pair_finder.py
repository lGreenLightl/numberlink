class PairFinder:
    def __init__(self, initial=None):
        self.dictionary = initial or {}

    def find(self, first):
        """ finds elements pair """
        if self.dictionary.get(first, first) == first:
            return first
        pair = self.find(self.dictionary.get(first, first))
        self.dictionary[first] = pair
        return pair

    def pair(self, first, second):
        """ set elements pair """
        a_pair, b_pair = self.find(first), self.find(second)
        self.dictionary[a_pair] = b_pair
