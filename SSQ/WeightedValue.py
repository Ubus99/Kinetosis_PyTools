class WeightedValue:
    val = 0
    weight = 1

    def __init__(self, weight):
        self.weight = weight

    def add(self, inp: int):
        self.val += inp * self.weight
