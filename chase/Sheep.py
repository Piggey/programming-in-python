from point2d import Point2D 
from random import choice

class Sheep:
    sheep_id: int 
    pos: Point2D
    move_dist: float 

    def __init__(self, sheep_id: int, pos_x: float, pos_y: float, move_dist: float):
        self.sheep_id = sheep_id
        self.pos = Point2D(pos_x, pos_y)
        self.move_dist = move_dist

    def get_current_position(self) -> (float, float):
        return (self.pos.x, self.pos.y)

    def move(self):
        possible_directions = [
            Point2D(1,  0),  # left
            Point2D(-1, 0),  # right
            Point2D(0,  1),  # up
            Point2D(0, -1),  # down
        ]

        direction = choice(possible_directions)

        self.pos += direction * self.move_dist