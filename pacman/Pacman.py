import random
from abc import ABC, abstractmethod
from .Direction import Direction


class Pacman(ABC):
    @abstractmethod
    def make_move(self, game_state, invalid_move=False) -> Direction:
        pass

    @abstractmethod
    def give_points(self, points):
        pass

    @abstractmethod
    def on_death(self):
        pass


class RandomPacman(Pacman):
    def give_points(self, points):
        pass

    def on_death(self):
        pass

    def make_move(self, game_state, invalid_move=False) -> Direction:
        return random.choice(list(Direction))  # it will make some valid move at some point
