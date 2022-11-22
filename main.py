from pacman.Ghost import Ghosts
from pacman.Pacman import RandomPacman
from pacman.Game import Game

board = ["*   g",
         "gwww ",
         " w*  ",
         " www ",
         "p + p"]

board_big = ["wwwwwwwwwwwwwwwwwwwwwwwwwwww",
             "wp***********ww***********pw",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w+wwww*wwwww*ww*wwwww*wwww+w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w**************************w",
             "w*wwww*ww*wwwwwwww*ww*wwww*w",
             "w*wwww*ww*wwwwwwww*ww*wwww*w",
             "w******ww****ww****ww******w",
             "wwwwww*wwwww ww wwwww*wwwwww",
             "     w*wwwww ww wwwww*w     ",
             "     w*ww          ww*w     ",
             "     w*ww www  www ww*w     ",
             "wwwwww*ww wwwggwww ww*wwwwww",
             "      *   www  www   *      ",
             "wwwwww*ww wwwggwww ww*wwwwww",
             "     w*ww wwwwwwww ww*w     ",
             "     w*ww          ww*w     ",
             "     w*ww wwwwwwww ww*w     ",
             "wwwwww*ww wwwwwwww ww*wwwwww",
             "w************ww************w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w*wwww*wwwww*ww*wwwww*wwww*w",
             "w+**ww****************ww**+w",
             "www*ww*ww*wwwwwwww*ww*ww*www",
             "www*ww*ww*wwwwwwww*ww*ww*www",
             "w******ww****ww****ww******w",
             "w*wwwwwwwwww*ww*wwwwwwwwww*w",
             "w*wwwwwwwwww*ww*wwwwwwwwww*w",
             "wp************************pw",
             "wwwwwwwwwwwwwwwwwwwwwwwwwwww"]

while True:
    game = Game(board_big, [Ghosts.RED, Ghosts.PINK, Ghosts.BLUE, Ghosts.ORANGE],
                [RandomPacman(), RandomPacman(), RandomPacman(), RandomPacman()], True, delay=False)
    game.run()
