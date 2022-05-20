class Size:
    def __init__(self, size) -> None:
        if len(size) > 1:
            self.Weight: int = size[0]
            self.Height: int = size[1]
        else:
            self.Weight: int = size[0]
            self.Height: int = size[0]


