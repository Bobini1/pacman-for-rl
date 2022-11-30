from dataclasses import dataclass
from typing import List, Dict, Any, Set, Tuple
from .Position import Position

"""
All info you might need, I hope.
"""


@dataclass
class GameState:
    you: Dict[str, Any]
    other_pacmans: List[Dict[str, Any]]
    ghosts: List[Dict[str, Any]]
    points: Set[Position]
    big_points: Set[Position]
    walls: Set[Position]
    board_size: Tuple[int, int]
