from Sheep import Sheep

from point2d import Point2D
from math import inf
import logging

class Wolf:
    pos: Point2D
    move_dist: float 
    
    def __init__(self, pos_x: float, pos_y: float, move_dist: float):
        logging.debug('calling Wolf.__init__()')
        self.pos = Point2D(pos_x, pos_y)
        self.move_dist = move_dist

    def get_current_position(self) -> (float, float):
        logging.debug('calling Wolf.get_current_position()')
        logging.debug(f'function Wolf.get_current_position() returned {str([self.pos.x, self.pos.y])}')
        return (self.pos.x, self.pos.y)

    def move(self, sheep_flock: list) -> (int, bool):
        logging.debug('calling Wolf.move()')

        # find closest sheep
        min_dist = inf
        closest_sheep: Sheep = None

        for sheep in sheep_flock:
            if (sheep is None):
                continue

            dist = (self.pos - sheep.pos).r
            if (dist < min_dist):
                min_dist = dist
                closest_sheep = sheep

        # eat sheep if within move_dist
        if (self.move_dist >= min_dist):
            self.pos = sheep_flock[closest_sheep.sheep_id].pos

            logging.info(f'Wolf has eaten sheep #{closest_sheep.sheep_id}')
            logging.debug(f'function Wolf.move() returned {str([closest_sheep.sheep_id, True])}')
            return (closest_sheep.sheep_id, True)

        # else move towards the targeted sheep 
        direction = closest_sheep.pos - self.pos
        direction.r = 1 # normalize the vector
        self.pos += direction * self.move_dist

        logging.debug(f'function Wolf.move() returned {str([closest_sheep.sheep_id, False])}')
        return (closest_sheep.sheep_id, False)
