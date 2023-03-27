import random

class NodeID:
    def __init__(self, id=None):
        self.id = id or random.getrandbits(160)

    def distance(self, other):
        return self.id ^ other.id
