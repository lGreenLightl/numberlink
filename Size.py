class Size:
    def __init__(self, size):
        if len(size) > 1:
            self.Weight = size[0]
            self.Height = size[1]
        else:
            self.Weight = size[0]
            self.Height = size[0]


