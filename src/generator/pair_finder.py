class PairFinder:
    def __init__(self, initial=None):
        self.pf = initial or {}

    def find(self, first):
        if self.pf.get(first, first) == first:
            return first
        pair = self.find(self.pf.get(first, first))
        self.pf[first] = pair
        return pair

    def pair(self, first, second):
        a_pair, b_pair = self.find(first), self.find(second)
        self.pf[a_pair] = b_pair
