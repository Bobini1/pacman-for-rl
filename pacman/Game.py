import operator

import pygame
from typing import List
from .Position import Position
from .Direction import Direction
from .GameState import GameState
from copy import deepcopy
from .Helpers import can_move_in_direction, direction_to_new_position

BIG_POINT_VALUE = 5
POINT_VALUE = 1
ENEMY_VALUE = 20
TIMER = 10


def my_itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return obj[item],
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g


class Game:
    def __init__(self, board: List[str], ghosts, players, display_mode_on=False):
        self.board = board
        self.display_mode_on = display_mode_on

        self.players = players
        self.ghosts = ghosts

        self.cell_size = 60

        self.screen = None
        self.player_image = None
        self.ghost_image = None
        self.board_size = None

        self.positions = {}
        self.directions = {}
        self.eatable_timers = {}
        self.walls = set()
        self.points = set()
        self.big_points = set()

        self.__init_game()

    def __init_game(self):
        ghosts_copy = self.ghosts.copy()
        players_copy = self.players.copy()

        for y, line in enumerate(self.board):
            for x, obj in enumerate(line):
                if obj == 'p':
                    player = players_copy.pop()
                    self.positions[player] = Position(x, y)
                    self.directions[player] = Direction.RIGHT
                if obj == 'g':
                    ghost = ghosts_copy.pop()
                    self.positions[ghost] = Position(x, y)
                    self.directions[ghost] = Direction.RIGHT
                if obj == '*':
                    self.points.add(Position(x, y))
                if obj == '+':
                    self.big_points.add(Position(x, y))
                if obj == 'w':
                    self.walls.add(Position(x, y))

        self.board_size = (len(self.board[0]), len(self.board))

        if self.display_mode_on:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 600))
            self.player_image = pygame.transform.scale(pygame.image.load('./assets/pacman.png'), (30, 30))
            self.ghost_image = pygame.transform.scale(pygame.image.load('./assets/red_ghost.png'), (30, 30))

    def __draw_board(self):
        self.screen.fill((0, 0, 0))

        for y, line in enumerate(self.board):
            for x, obj in enumerate(line):
                if obj == 'w':
                    color = (0, 255, 255)
                    pygame.draw.rect(self.screen, color, pygame.Rect(60 * x, 60 * y, 60, 60))

        color = (255, 255, 0)
        for player in self.players:
            position = self.positions[player]
            pygame.draw.rect(self.screen, color, pygame.Rect(60 * position.x, 60 * position.y, 60, 60))
            pygame.draw.rect(self.screen, color, pygame.Rect(position.x * self.cell_size + 15,
                                                             position.y * self.cell_size + 15, 30, 30))
            self.screen.blit(self.player_image,
                             (position.x * self.cell_size + 15, position.y * self.cell_size + 15))

        for ghost in self.ghosts:
            position = self.positions[ghost]
            # pygame.draw.rect(self.screen, color, pygame.Rect(ghost['x'] * self.cell_size + 15, ghost['y'] * self.cell_size + 15, 30, 30))
            self.screen.blit(self.ghost_image,
                             (position.x * self.cell_size + 15, position.y * self.cell_size + 15))

        color = (255, 255, 255)

        for point in self.points:
            pygame.draw.ellipse(self.screen, color,
                                pygame.Rect(point.x * self.cell_size + 25, point.y * self.cell_size + 25, 10,
                                            10))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.__draw_board()

            for entity in self.eatable_timers.keys():
                self.eatable_timers[entity] -= 1
                if self.eatable_timers[entity] == 0:
                    del self.eatable_timers[entity]

            player_info = {}
            for player in self.players:
                position = self.positions[player]
                if player in self.eatable_timers:
                    is_eatable = True
                    eatable_timer = self.eatable_timers[player]
                else:
                    is_eatable = False
                    eatable_timer = None
                player_info[player] = {'position': position, 'is_eatable': is_eatable, 'eatable_timer': eatable_timer}

            ghost_info = []
            for ghost in self.ghosts:
                position = self.positions[ghost]
                direction = self.directions[ghost]
                if ghost in self.eatable_timers:
                    is_eatable = True
                    eatable_timer = self.eatable_timers[ghost]
                else:
                    is_eatable = False
                    eatable_timer = None
                ghost_info.append({'position': position, 'is_eatable': is_eatable, 'eatable_timer': eatable_timer,
                                   'direction': direction})

            moves = {}

            for player in self.players:
                other_players = player_info.copy()
                you = other_players.pop(player)
                other_players = deepcopy(list(other_players.values()))
                you = deepcopy(you)
                ghosts = deepcopy(ghost_info)
                points = deepcopy(self.points)
                big_points = deepcopy(self.big_points)
                walls = deepcopy(self.walls)
                board_size = deepcopy(self.board_size)
                game_state = GameState(you, other_players, ghosts, points, big_points, walls, board_size)
                move = player.make_move(game_state)
                while True:
                    if can_move_in_direction(self.positions[player], move, self.walls, self.board_size):
                        moves[player] = move
                        break
                    else:
                        move = player.make_move(game_state, invalid_move=True)

            ghost_moves = {}
            for ghost in self.ghosts:
                itemgetter = my_itemgetter(*self.players)
                ghost_moves[ghost] = ghost.make_move(self.positions[ghost], self.directions[ghost], self.walls,
                                                     itemgetter(self.positions), self.board_size,
                                                     True if ghost in self.eatable_timers else False)
            # convert moves to positions
            for player in self.players:
                self.positions[player] = direction_to_new_position(self.positions[player], moves[player])

            for ghost in self.ghosts:
                self.positions[ghost] = direction_to_new_position(self.positions[ghost], ghost_moves[ghost])

            # handle eating enemies
            # the time complexity could be improved but I don't care
            for player in self.players:
                if player in self.eatable_timers:
                    continue
                # eating ghosts
                for ghost in self.ghosts:
                    if self.positions[player] == self.positions[ghost]:
                        if ghost in self.eatable_timers:
                            self.eatable_timers.pop(ghost)
                            self.positions[ghost] = ghost.starting_position
                            self.positions.pop(ghost)
                            self.directions[ghost] = Direction.RIGHT
                            player.give_points(ENEMY_VALUE)
                        else:
                            self.eatable_timers.pop(player, None)
                            self.players.remove(player)
                            self.positions.pop(player)
                            self.directions.pop(player)
                            player.on_death()
                # eating players
                for other_player in self.players:
                    if player is not other_player:
                        if self.positions.get(player) == self.positions.get(other_player):
                            if other_player in self.eatable_timers:
                                self.eatable_timers.pop(other_player)
                                self.players.remove(other_player)
                                self.positions.pop(other_player)
                                self.directions.pop(other_player)
                                other_player.on_death()
            # ghosts eating players
            for ghost in self.ghosts:
                if ghost in self.eatable_timers:
                    continue
                for player in self.players:
                    if self.positions[ghost] == self.positions[player]:
                        self.eatable_timers.pop(player)
                        self.players.remove(player)
                        self.positions.pop(player)
                        self.directions.pop(player)
                        player.on_death()

            if not self.players:  # bye
                break

            # eating points
            for player in self.players:
                if self.positions[player] in self.points:
                    self.points.remove(self.positions[player])
                    player.give_points(POINT_VALUE)
                if self.positions[player] in self.big_points:
                    self.big_points.remove(self.positions[player])
                    # set timer on other players and ghosts
                    for other_player in self.players:
                        if other_player is not player:
                            self.eatable_timers[other_player] = TIMER
                    for ghost in self.ghosts:
                        self.eatable_timers[ghost] = TIMER
                    player.give_points(BIG_POINT_VALUE)

            if not self.points and not self.big_points:  # congrats!
                break

            pygame.time.delay(100)
