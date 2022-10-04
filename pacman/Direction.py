from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __invert__(self):
        return {self.UP: self.DOWN, self.DOWN: self.UP, self.LEFT: self.RIGHT, self.RIGHT: self.LEFT}[self]
