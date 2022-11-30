import random

import pygame
from typing import List

from .Ghost import Ghost
from .Pacman import Pacman
from .Position import Position
from .Direction import Direction
from .GameState import GameState
from copy import deepcopy
from .Helpers import can_move_in_direction, direction_to_new_position

BIG_POINT_VALUE = 5
BIG_BIG_POINT_VALUE = 20
POINT_VALUE = 1
ENEMY_VALUE = 20
TIMER = 15
TIMER_SPAWNER = TIMER * 3


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
    def __init__(self, board: List[str], ghosts: List[Ghost], players: List[Pacman], display_mode_on=False, delay=100):
        self.board = board
        self.display_mode_on = display_mode_on
        self.delay = delay

        self.players = players
        self.ghosts = ghosts

        self.cell_size = 550 // (len(board[0]))

        self.player_size = self.cell_size // 2
        self.point_size = self.cell_size // 6
        self.big_point_size = self.cell_size // 3
        self.big_big_point_size = self.cell_size // 2

        self.screen = None
        self.player_image = None
        self.ghost_image = None
        self.board_size = None

        self.positions = {}
        self.starting_positions = {}
        self.directions = {}
        self.eatable_timers = {}
        self.phasing_timers = {}
        self.double_points_timers = {}
        self.indestructible_timers = {}
        self.spawners_timers = {}
        self.walls = set()
        self.points = set()
        self.big_points = set()
        self.big_big_points = set()
        self.phasing_points = set()
        self.indestructible_points = set()
        self.double_points = set()
        self.regenerate_points = set()
        self.spawners = set()

        self.final_scores = {player: 0 for player in self.players}

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
                    self.starting_positions[ghost] = Position(x, y)
                    self.directions[ghost] = Direction.RIGHT
                if obj == '*':
                    self.points.add(Position(x, y))
                if obj == '+':
                    self.big_points.add(Position(x, y))
                if obj == 'w':
                    self.walls.add(Position(x, y))
                if obj == 'z':
                    self.phasing_points.add(Position(x, y))
                if obj == 'i':
                    self.indestructible_points.add(Position(x, y))
                if obj == 'd':
                    self.double_points.add(Position(x, y))
                if obj == 's':
                    self.spawners.add(Position(x, y))
                if obj == 'b':
                    self.big_big_points.add(Position(x, y))

        for spawner in self.spawners:
            self.spawners_timers[spawner] = TIMER_SPAWNER, False

        self.board_size = (len(self.board[0]), len(self.board))

        if self.display_mode_on:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 600))
            self.player_image = pygame.transform.scale(pygame.image.load('./assets/pacman.png'), (30, 30))
            self.ghost_image = pygame.transform.scale(pygame.image.load('./assets/red_ghost.png'), (30, 30))
            self.ghost_image_blue = pygame.transform.scale(pygame.image.load('./assets/blue_ghost.png'), (30, 30))

    def __draw_board(self):
        self.screen.fill((0, 0, 0))

        for y, line in enumerate(self.board):
            for x, obj in enumerate(line):
                if obj == 'w':
                    color = (0, 255, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(self.cell_size * x, self.cell_size * y, self.cell_size,
                                                 self.cell_size))

        for player in self.players:
            color = (0, 0, 255) if player in self.eatable_timers else (255, 255, 0)
            position = self.positions[player]
            pygame.draw.rect(self.screen, color,
                             pygame.Rect(self.cell_size * position.x, self.cell_size * position.y, self.cell_size,
                                         self.cell_size))
            pygame.draw.rect(self.screen, color, pygame.Rect(position.x * self.cell_size + self.player_size // 2,
                                                             position.y * self.cell_size + self.player_size // 2,
                                                             self.player_size, self.player_size))
            self.screen.blit(self.player_image,
                             (position.x * self.cell_size - self.player_size // 2,
                              position.y * self.cell_size - self.player_size // 2))

        for ghost in self.ghosts:
            position = self.positions[ghost]
            self.screen.blit(self.ghost_image_blue if ghost in self.eatable_timers else self.ghost_image,
                             (position.x * self.cell_size - self.player_size // 2,
                              position.y * self.cell_size - self.player_size // 2))

        color = (255, 255, 255)

        for point in self.points:
            pygame.draw.ellipse(self.screen, color,
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.point_size) // 2,
                                            self.point_size,
                                            self.point_size))
        for point in self.big_points:
            pygame.draw.ellipse(self.screen, color,
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            self.big_point_size,
                                            self.big_point_size))

        for point in self.phasing_points:
            pygame.draw.ellipse(self.screen, (255, 0, 255),
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            self.big_point_size,
                                            self.big_point_size))

        for point in self.double_points:
            pygame.draw.ellipse(self.screen, (255, 255, 0),
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            self.big_point_size,
                                            self.big_point_size))

        for point in self.indestructible_points:
            pygame.draw.ellipse(self.screen, (0, 255, 0),
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.big_point_size) // 2,
                                            self.big_point_size,
                                            self.big_point_size))

        for point in self.big_big_points:
            pygame.draw.ellipse(self.screen, (255, 0, 0),
                                pygame.Rect(point.x * self.cell_size + (self.cell_size - self.big_big_point_size) // 2,
                                            point.y * self.cell_size + (self.cell_size - self.big_big_point_size) // 2,
                                            self.big_big_point_size,
                                            self.big_big_point_size))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.__draw_board()

            pygame.time.delay(self.delay)

            if not self.players:  # bye
                print("you lost")
                return self.final_scores

            if not self.points and not self.big_points:  # congrats!
                print('you won')
                return self.final_scores

            self.update_eatable_timers()

            self.update_phasing_timers()

            self.update_double_points_timers()

            self.update_indestructible_timers()

            self.update_spawners_timers()

            player_info = self.get_player_info()

            ghost_info = self.get_ghost_info()

            moves = self.get_player_moves(ghost_info, player_info)

            self.update_ghost_movement_directions()

            old_positions = self.update_positions_and_get_old(moves)

            points_to_give = {player: 0 for player in self.players}

            self.handle_players_eating_enemies(old_positions, points_to_give)

            # ghosts eating players
            self.handle_ghosts_eating(old_positions)

            # eating points
            self.handle_players_eating_points(points_to_give)

            for player, points in points_to_give.items():
                if player in self.players:  # if player is not dead
                    player.give_points(points)
                    self.final_scores[player] += points

    def handle_players_eating_points(self, points_to_give):
        for player in self.players:
            if self.positions[player] in self.points:
                self.points.remove(self.positions[player])
                points_to_give[
                    player] += POINT_VALUE * 1 if player not in self.double_points_timers else POINT_VALUE * 2
            if self.positions[player] in self.big_points:
                self.big_points.remove(self.positions[player])
                # set timer on other players and ghosts
                for other_player in self.players:
                    if other_player is not player:
                        self.eatable_timers[other_player] = TIMER
                for ghost in self.ghosts:
                    self.eatable_timers[ghost] = TIMER
                points_to_give[
                    player] += BIG_POINT_VALUE * 1 if player not in self.double_points_timers else BIG_POINT_VALUE * 2
            if self.positions[player] in self.phasing_points:
                self.phasing_points.remove(self.positions[player])
                self.phasing_timers[player] = TIMER
            if self.positions[player] in self.double_points:
                self.double_points.remove(self.positions[player])
                self.double_points_timers[player] = TIMER
            if self.positions[player] in self.indestructible_points:
                self.indestructible_points.remove(self.positions[player])
                self.indestructible_timers[player] = TIMER
            if self.positions[player] in self.big_big_points:
                self.big_big_points.remove(self.positions[player])
                points_to_give[
                    player] += BIG_BIG_POINT_VALUE * 1 if player not in self.double_points_timers else BIG_BIG_POINT_VALUE * 2

    def handle_ghosts_eating(self, old_positions):
        for ghost in self.ghosts:
            if ghost in self.eatable_timers:
                continue
            for player in self.players:
                if player in self.indestructible_timers:
                    continue
                if self.positions.get(ghost) == self.positions.get(player) or (
                        self.positions.get(ghost) == old_positions[
                    player] and  # for the case where a player and ghost
                        self.positions.get(player) == old_positions[ghost]  # move over each other in the same tick
                ):
                    self.remove_player(player)

    def remove_player(self, player):
        self.eatable_timers.pop(player, None)
        if player in self.players:
            self.players.remove(player)
        self.positions.pop(player, None)
        self.directions.pop(player, None)
        player.on_death()

    def handle_players_eating_enemies(self, old_positions, points_to_give):
        players_to_remove = []
        # handle eating enemies
        # the time complexity could be improved but I don't care
        for player in self.players:
            if player in self.eatable_timers:
                continue
            # eating ghosts
            self.handle_players_eating_ghosts(old_positions, player, players_to_remove, points_to_give)
            # eating players
            self.handle_players_eating_players(old_positions, player, players_to_remove, points_to_give)

        for player in players_to_remove:
            self.remove_player(player)

    def handle_players_eating_players(self, old_positions, player, players_to_remove, points_to_give):
        for other_player in self.players:
            if player is not other_player:
                if self.positions.get(player) == self.positions.get(other_player) or (
                        self.positions.get(player) == old_positions[other_player]
                        and self.positions.get(other_player) == old_positions[player]
                ):
                    if other_player in self.eatable_timers and other_player not in self.indestructible_timers:
                        players_to_remove.append(other_player)
                        points_to_give[
                            player] += ENEMY_VALUE * 1 if player not in self.double_points_timers else ENEMY_VALUE * 2
                    elif player not in self.indestructible_timers:
                        # don't crash into each other. (^^)
                        players_to_remove.append(player)

    def handle_players_eating_ghosts(self, old_positions, player, players_to_remove, points_to_give):
        for ghost in self.ghosts:
            if self.positions[player] == self.positions[ghost] or (
                    self.positions.get(player) == old_positions[ghost]
                    and self.positions.get(ghost) == old_positions[player]
            ):
                if ghost in self.eatable_timers:
                    self.kill_ghost(ghost, player, points_to_give)
                else:
                    players_to_remove.append(player)

    def kill_ghost(self, ghost, player, points_to_give):
        self.eatable_timers.pop(ghost)
        self.positions[ghost] = self.starting_positions[ghost]
        self.directions[ghost] = Direction.RIGHT
        points_to_give[player] += ENEMY_VALUE * 1 if player not in self.double_points_timers else ENEMY_VALUE * 2

    def update_positions_and_get_old(self, moves):
        old_positions = {}
        # convert moves to positions
        for player in self.players:
            old_positions[player] = self.positions[player]
            self.positions[player] = direction_to_new_position(self.positions[player], moves[player])
        for ghost in self.ghosts:
            old_positions[ghost] = self.positions[ghost]
            self.positions[ghost] = direction_to_new_position(self.positions[ghost], self.directions[ghost])
        return old_positions

    def update_ghost_movement_directions(self):
        for ghost in self.ghosts:
            itemgetter = my_itemgetter(*self.players)
            self.directions[ghost] = ghost.make_move(self.positions[ghost], self.directions[ghost], self.walls,
                                                     itemgetter(self.positions), self.board_size,
                                                     True if ghost in self.eatable_timers else False)

    def get_player_moves(self, ghost_info, player_info):
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
            is_stuck = self.is_stuck(player)
            move = player.make_move(game_state)
            while True:
                if can_move_in_direction(self.positions[player], move, self.walls, self.board_size,
                                         phasing=is_stuck or player in self.phasing_timers):
                    moves[player] = move
                    break
                else:
                    move = player.make_move(game_state, invalid_move=True)

        return moves

    def is_stuck(self, player):
        is_stuck = True
        for direction in Direction:
            if can_move_in_direction(self.positions[player], direction, self.walls, self.board_size):
                is_stuck = False
                break
        return is_stuck

    def get_ghost_info(self):
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
        return ghost_info

    def get_player_info(self):
        player_info = {}
        for player in self.players:
            position = self.positions[player]
            if player in self.eatable_timers:
                is_eatable = True
                eatable_timer = self.eatable_timers[player]
            else:
                is_eatable = False
                eatable_timer = None
            if player in self.phasing_timers or self.is_stuck(player):
                is_phasing = True
                phasing_timer = self.phasing_timers.get(player, 0)
            else:
                is_phasing = False
                phasing_timer = None
            if player in self.double_points_timers:
                is_double_points = True
                double_points_timer = self.double_points_timers.get(player, 0)
            else:
                is_double_points = False
                double_points_timer = None
            if player in self.indestructible_timers:
                is_indestructible = True
                indestructible_timer = self.indestructible_timers.get(player, 0)
            else:
                is_indestructible = False
                indestructible_timer = None
            player_info[player] = {'position': position, 'is_eatable': is_eatable, 'eatable_timer': eatable_timer,
                                   'is_phasing': is_phasing, 'phasing_timer': phasing_timer,
                                   'is_double_points': is_double_points, 'double_points_timer': double_points_timer,
                                   'is_indestructible': is_indestructible, 'indestructible_timer': indestructible_timer}
        return player_info

    def update_eatable_timers(self):
        timers_to_remove = []
        for entity in self.eatable_timers.keys():
            self.eatable_timers[entity] -= 1
            if self.eatable_timers[entity] == 0:
                timers_to_remove.append(entity)
        for entity in timers_to_remove:
            del self.eatable_timers[entity]

    def update_phasing_timers(self):
        timers_to_remove = []
        for entity in self.phasing_timers.keys():
            self.phasing_timers[entity] -= 1
            if self.phasing_timers[entity] == 0:
                timers_to_remove.append(entity)
        for entity in timers_to_remove:
            del self.phasing_timers[entity]

    def update_double_points_timers(self):
        timers_to_remove = []
        for entity in self.double_points_timers.keys():
            self.double_points_timers[entity] -= 1
            if self.double_points_timers[entity] == 0:
                timers_to_remove.append(entity)
        for entity in timers_to_remove:
            del self.double_points_timers[entity]

    def update_indestructible_timers(self):
        timers_to_remove = []
        for entity in self.indestructible_timers.keys():
            self.indestructible_timers[entity] -= 1
            if self.indestructible_timers[entity] == 0:
                timers_to_remove.append(entity)
        for entity in timers_to_remove:
            del self.indestructible_timers[entity]

    def update_spawners_timers(self):
        for position in self.spawners_timers.keys():
            timer_value = self.spawners_timers[position]
            self.spawners_timers[position] = (timer_value[0] - 1, timer_value[1])

            if self.spawners_timers[position][1] and position not in (
                    self.phasing_points | self.double_points | self.indestructible_points):  # if point was eaten
                self.spawners_timers[position] = TIMER_SPAWNER, False

            if self.spawners_timers[position][0] == 0:
                if self.spawners_timers[position][1]:
                    self.remove_point(position)
                    self.spawners_timers[position] = TIMER_SPAWNER, False
                else:
                    random.choice([self.phasing_points, self.double_points, self.indestructible_points, self.big_big_points]).add(position)
                    self.spawners_timers[position] = TIMER_SPAWNER, True

    def remove_point(self, position):
        self.spawners_timers[position] = TIMER_SPAWNER, False
        self.indestructible_points.discard(position)
        self.indestructible_timers.pop(position, None)
        self.double_points.discard(position)
        self.double_points_timers.pop(position, None)
        self.phasing_points.discard(position)
        self.phasing_timers.pop(position, None)
        self.big_big_points.discard(position)
