import pygame

board = ["*   g",
         " www ",
         " w*  ",
         " www ",
         "p    "]

game = Game(board, [Player(), Player()], [Ghost(), Ghost()], True)
