from pacman.Ghost import Ghosts
from pacman.Pacman import RandomPacman
from pacman.Game import Game

board = ["*   g",
         "gwww ",
         " w*  ",
         " www ",
         "p + p"]

game = Game(board, [Ghosts.RED, Ghosts.PINK], [RandomPacman(), RandomPacman()], True)
game.run()
