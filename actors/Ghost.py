

class Ghost:
    def __init__(self, strategy_normal, strategy_eatable):
        self.strategy_normal = strategy_normal
        self.strategy_eatable = strategy_eatable

    def move(self, my_position, my_direction, walls, pacman_positions, is_eatable):
        if is_eatable:
            return self.strategy_eatable.move(my_position, my_direction, walls, pacman_positions)
        else:
            return self.strategy_normal.move(my_position, my_direction, walls, pacman_positions)

