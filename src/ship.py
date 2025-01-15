class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []
        self.hits = []

    def is_sunk(self):
        return len(self.hits) == self.size