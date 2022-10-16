from dataclasses import dataclass
from typing import List, Dict, Any, Set, Tuple
from .Position import Position


"""
All info you might need, I hope.
"""
@dataclass
class GameState:
    you: Dict[str, Any]  # {'position': position, 'is_eatable': is_eatable, 'eatable_timer': eatable_timer}
    other_pacmans: List[Dict[str, Any]]  # same as above but a list
    ghosts: List[Dict[str, Any]]  # {'position': position, 'is_eatable': is_eatable, 'eatable_timer': eatable_timer, direction': direction}
    points: Set[Position]
    big_points: Set[Position]
    walls: Set[Position]
    board_size: Tuple[int, int]
