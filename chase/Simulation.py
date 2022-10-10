from Sheep import Sheep
from Wolf import Wolf

from configparser import ConfigParser

class Simulation:

    def __init__(self, simulation_arguments: list):
        self.init_args = simulation_arguments
        self.reset()

    def start(self):
        pass

    def reset(self):
        # set everything to default 
        self.init_pos_limit:  float = 10.0
        self.sheep_move_dist: float = 0.5
        self.wolf_move_dist:  float = 1.0

        self.end_of_sim:       bool = False
        self.max_rounds:        int = 50

        # try reading from config file 
        if (self.init_args.config):
            config_filename = self.init_args.config[0]
            config = ConfigParser().read(config_filename)

            new_init_pos_limit = float(config['Terrain']['InitPosLimit'])
            if (new_init_pos_limit < 0):
                raise ValueError(f'InitPosLimit in config file {config_filename} is less than zero.')

            new_sheep_move_dist = float(config['Movement']['SheepMoveDist'])
            if (new_sheep_move_dist < 0):
                raise ValueError(f'SheepMoveDist in config file {config_filename} is less than zero.')

            new_wolf_move_dist = float(config['Movement']['WolfMoveDist'])
            if (new_wolf_move_dist < 0):    
                raise ValueError(f'WolfMoveDist in config file {config_filename} is less than zero.')

            self.init_pos_limit = new_init_pos_limit
            self.sheep_move_dist = new_sheep_move_dist
            self.wolf_move_dist = new_wolf_move_dist


    def __run_simulation_step(self):
        pass

    def __export_animal_locations(self, filename: str):
        pass

    def __export_sheep_count(self, filename: str):
        pass
