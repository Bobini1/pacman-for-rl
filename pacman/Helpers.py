from .Position import Position, clamp
from .Direction import Direction
from typing import List, Set, Tuple


def can_move_in_direction(position: Position, direction: Direction, walls: Set[Position],
                          board_size: Tuple[int, int], phasing=False) -> bool:
    return direction_to_new_position(position, direction, board_size) not in walls or phasing


def direction_to_new_position(position: Position, direction: Direction, board_size: Tuple[int, int]) -> Position:
    if direction == Direction.UP:
        if position.y == 0:
            return Position(position.x, board_size[1] - 1)
        return Position(position.x, position.y - 1)
    elif direction == Direction.DOWN:
        if position.y == board_size[1] - 1:
            return Position(position.x, 0)
        return Position(position.x, position.y + 1)
    elif direction == Direction.LEFT:
        if position.x == 0:
            return Position(board_size[0] - 1, position.y)
        return Position(position.x - 1, position.y)
    elif direction == Direction.RIGHT:
        if position.x == board_size[0] - 1:
            return Position(0, position.y)
        return Position(position.x + 1, position.y)
    else:
        return position


def positions_to_direction(start: Position, end: Position, board_size: Tuple[int, int]) -> Direction:
    if start.x == 0 and end.x == board_size[0] - 1:
        return Direction.LEFT
    elif start.x == board_size[0] - 1 and end.x == 0:
        return Direction.RIGHT
    elif start.y == 0 and end.y == board_size[1] - 1:
        return Direction.UP
    elif start.y == board_size[1] - 1 and end.y == 0:
        return Direction.DOWN
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
# get closest position to start that is not a wall
def get_closest_position(start: Position, walls: Set[Position], board_size: Tuple[int, int]) -> Position:
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
        if current not in walls and current == clamp(
                current, Position(0, 0), Position(board_size[0] - 1, board_size[1] - 1)
        ):
            # return the current position
            return current

        # for each direction
        for direction in Direction:
            # get the new position
            new_position = direction_to_new_position(current, direction, board_size)

            # if the new position is not visited
            if new_position == clamp(
                    new_position, Position(0, 0), Position(board_size[0] - 1, board_size[1] - 1)) and not \
            visited[new_position.x][new_position.y]:
                # add the new position to the queue
                queue.append(new_position)

                # mark the new position as visited
                visited[new_position.x][new_position.y] = True

    # return the start position
    return start


# path finding algorithm between two positions on board
def find_path(start: Position, end: Position, walls: Set[Position], board_size: Tuple[int, int]) -> List[Position]:
    start = Position(start.x % board_size[0], start.y % board_size[1])

    end = Position(end.x % board_size[0], end.y % board_size[1])

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
            new_position = direction_to_new_position(current, direction, board_size)

            # if the new position is not a wall and is not visited
            if new_position not in walls and not \
                    visited[new_position.x][new_position.y]:
                # add the new position to the queue
                queue.append(new_position)

                # mark the new position as visited
                visited[new_position.x][new_position.y] = True

                # set the parent of the new position
                parent[new_position.x][new_position.y] = current

    # return an empty path
    return []
