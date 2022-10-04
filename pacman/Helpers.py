from .Position import Position, clamp
from .Direction import Direction
from typing import List, Dict, Any, Set, Tuple


def can_move_in_direction(position: Position, direction: Direction, walls: Set[Position],
                          board_size: Tuple[int, int]) -> bool:
    pos = None
    if direction == Direction.UP:
        pos = Position(position.x, position.y - 1)
    elif direction == Direction.DOWN:
        pos = Position(position.x, position.y + 1)
    elif direction == Direction.LEFT:
        pos = Position(position.x - 1, position.y)
    elif direction == Direction.RIGHT:
        pos = Position(position.x + 1, position.y)

    return pos not in walls and pos == clamp(pos, Position(0, 0), Position(board_size[0] - 1, board_size[1] - 1))


def direction_to_new_position(position: Position, direction: Direction) -> Position:
    if direction == Direction.UP:
        return Position(position.x, position.y - 1)
    elif direction == Direction.DOWN:
        return Position(position.x, position.y + 1)
    elif direction == Direction.LEFT:
        return Position(position.x - 1, position.y)
    elif direction == Direction.RIGHT:
        return Position(position.x + 1, position.y)
    else:
        print(direction)
        raise Exception("Unknown direction")


def positions_to_direction(start: Position, end: Position) -> Direction:
    if start.x == end.x:
        if start.y > end.y:
            return Direction.UP
        else:
            return Direction.DOWN
    elif start.x > end.x:
        return Direction.LEFT
    else:
        return Direction.RIGHT


# get closest position to start that is not a wall
def get_closest_position(start: Position, walls: Set[Position], board_size: Tuple[int, int]) -> Position:
    # get the board size
    board_width, board_height = board_size

    # create a visited array
    visited = [[False for _ in range(board_height)] for _ in range(board_width)]

    # create a queue
    queue = []

    # add the start position to the queue
    queue.append(start)

    # mark the start position as visited
    visited[start.x][start.y] = True

    # while the queue is not empty
    while len(queue) > 0:
        # get the first element from the queue
        current = queue.pop(0)

        # if the current position is not a wall
        if current not in walls:
            # return the current position
            return current

        # for each direction
        for direction in Direction:
            # get the new position
            new_position = direction_to_new_position(current, direction)

            # if the new position is not visited
            if not visited[new_position.x][new_position.y]:
                # add the new position to the queue
                queue.append(new_position)

                # mark the new position as visited
                visited[new_position.x][new_position.y] = True

    # return the start position
    return start


# path finding algorithm between two positions on board
def find_path(start: Position, end: Position, walls: Set[Position], board_size: Tuple[int, int]) -> List[Position]:
    # get the board size
    board_width, board_height = board_size

    # create a visited array
    visited = [[False for _ in range(board_height)] for _ in range(board_width)]

    # create a parent array
    parent = [[None for _ in range(board_height)] for _ in range(board_width)]

    # create a queue
    queue = []

    # get the closest position to end that is not a wall
    end = get_closest_position(end, walls, board_size)

    # add the start position to the queue
    queue.append(start)

    # mark the start position as visited
    visited[start.x][start.y] = True

    # while the queue is not empty
    while len(queue) > 0:
        # get the first element from the queue
        current = queue.pop(0)

        # if the current position is the end position
        if current == end:
            # create a path
            path = []

            # while the current position is not the start position
            while current != start:
                # add the current position to the path
                path.append(current)

                # get the parent of the current position
                current = parent[current.x][current.y]

            # reverse the path
            path.reverse()

            # return the path
            return path

        # for each direction
        for direction in Direction:
            # get the new position
            new_position = direction_to_new_position(current, direction)

            # if the new position is not a wall and is not visited
            if new_position == clamp(
                    new_position, Position(0, 0),
                    Position(board_size[0] - 1, board_size[1] - 1)) and new_position not in walls and not \
                    visited[new_position.x][new_position.y]:
                # add the new position to the queue
                queue.append(new_position)

                # mark the new position as visited
                visited[new_position.x][new_position.y] = True

                # set the parent of the new position
                parent[new_position.x][new_position.y] = current

    # return an empty path
    return []
