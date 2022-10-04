from abc import ABC, abstractmethod
from Direction import Direction
from fractions import Fraction


class Actor(ABC):
    @abstractmethod
    def make_move(self, game_state) -> Direction:
        pass

    @abstractmethod
    def give_points(self, points):
        pass

    @abstractmethod
    def on_death(self):
        pass

    @abstractmethod
    def respawns(self) -> bool:
        pass

    @abstractmethod
    def spawn_position(self):
        pass



