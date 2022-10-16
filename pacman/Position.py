from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Position:
    x: int
    y: int

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


def clamp(val: Position, low: Position, high: Position):
    returned = deepcopy(val)
    if val.x < low.x:
        returned.x = low.x
    elif val.x > high.x:
        returned.x = high.x
    if val.y < low.y:
        returned.y = low.y
    elif val.y > high.y:
        returned.y = high.y
    return returned
