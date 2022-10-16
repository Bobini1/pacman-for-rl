import random
from abc import ABC, abstractmethod
from .Direction import Direction


"""
A pacman is that yellow thing with a big mouth that can eat points and ghosts!
In this game, there can be more than one pacman and they can eat each other too.
"""
class Pacman(ABC):
    """
    Make your choice!
    You can make moves completely randomly if you want, the game won't allow you to make an invalid move.
    That's what invalid_move is for - it will be true if your previous choice was invalid.
    """
    @abstractmethod
    def make_move(self, game_state, invalid_move=False) -> Direction:
        pass

    """
    The game will call this once for each pacman at each time step.
    """
    @abstractmethod
    def give_points(self, points):
        pass

    """
    Do whatever you want with this info. The game will continue until all pacmans die or all points are eaten.
    """
    @abstractmethod
    def on_death(self):
        pass


"""
I hope yours will be smarter than this one...
"""
class RandomPacman(Pacman):
    def give_points(self, points):
        print(f"random pacman got {points} points")

    def on_death(self):
        print("random pacman dead")

    def make_move(self, game_state, invalid_move=False) -> Direction:
        return random.choice(list(Direction))  # it will make some valid move at some point
