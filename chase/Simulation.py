from Sheep import Sheep
from Wolf import Wolf

from configparser import ConfigParser
from random import uniform
from os import mkdir
import logging
from json import dump
from csv import writer

# a way to continue with pressing any key 
try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

class Simulation:
    init_pos_limit: float
    sheep_move_dist: float 
    wolf_move_dist: float 

    max_rounds: int 
    flock_size: int 

    is_running: bool 

    def __init__(self, simulation_arguments: list):
        self.init_args = simulation_arguments
        self.reset()

    def start(self):
        locations = []
        alive = []
        for rnd in range(self.max_rounds):
            # cache animals' positions
            locations.append(self.__cache_animals_position(rnd))

            num_alive_sheep = sum(x is not None for x in self.sheep_flock)

            # cache number of alive sheep
            alive.append([rnd + 1, num_alive_sheep])

            # stop if theres no sheep left
            if (num_alive_sheep == 0):
                break

            # run simulation
            hunted_sheep_index, sheep_eaten = self.__run_simulation_step()
            self.__print_simulation_info(rnd + 1, num_alive_sheep, hunted_sheep_index, sheep_eaten)

        self.__export_animal_locations(self.output_dir + self.position_file, locations)
        self.__export_sheep_count(self.output_dir + self.alive_file, alive)

    def __cache_animals_position(self, rnd: int) -> dict:
        rnd_locations = {}
        rnd_locations['round_no'] = rnd + 1

        rnd_locations['wolf_pos'] = self.wolf.get_current_position()

        round_sheep_positions = []
        for sheep in self.sheep_flock:
            if (sheep is None):
                round_sheep_positions.append(None)
            else:
                round_sheep_positions.append(sheep.get_current_position())

        rnd_locations['sheep_pos'] = round_sheep_positions


        return rnd_locations
        
    def reset(self):
        # set everything to default 
        self.init_pos_limit:  float = 10.0
        self.sheep_move_dist: float = 0.5
        self.wolf_move_dist:  float = 1.0

        self.is_running:       bool = True
        self.max_rounds:        int = 50 
        self.flock_size:        int = 15

        self.output_dir:        str = ''
        self.log_file:          str = 'chase.log'
        self.position_file:     str = 'pos.json'
        self.alive_file:        str = 'alive.csv'

        # simulation variables from config file 
        if (self.init_args.config):
            config_filename = self.init_args.config[0]
            self.__read_from_config(config_filename)

        # output files directory
        if (self.init_args.dir):
            self.output_dir = self.init_args.dir[0]
            if (self.output_dir[-1] != '/'):
                self.output_dir += '/'

            # create directory if doesnt exist, ignore if it does
            try: mkdir(self.output_dir)
            except FileExistsError: pass

        # logging
        if (self.init_args.log):
            logging.basicConfig(
                level=self.init_args.log[0],
                filename=self.output_dir + self.log_file,
                filemode='w',
                format='%(name)s - %(levelname)s - %(message)s'
            )

        # max number of rounds
        if (self.init_args.rounds):
            self.max_rounds = self.init_args.rounds[0]

        # size of sheep flock
        if (self.init_args.sheep):
            self.flock_size = self.init_args.sheep[0]

        # whether to wait inbetween rounds
        self.wait = self.init_args.wait

        # init wolf and sheep
        self.wolf = Wolf(0, 0, self.wolf_move_dist)

        self.sheep_flock = []
        for i in range(self.flock_size):
            x = uniform(-self.init_pos_limit, self.init_pos_limit)
            y = uniform(-self.init_pos_limit, self.init_pos_limit)
            sheep = Sheep(i, x, y, self.sheep_move_dist)

            self.sheep_flock.append(sheep)

    def __print_simulation_info(self, current_round: int, alive_sheep: int, hunted_sheep_index: int, sheep_eaten: bool):
        print(f'ROUND {current_round}:')
        print(f"\twolf's position: [{self.wolf.pos.x:.3f}, {self.wolf.pos.y:.3f}]")

        if (sheep_eaten):
            alive_sheep -= 1
            print(f"\twolf has eaten sheep #{hunted_sheep_index}")
        else:
            print(f"\twolf is currently chasing sheep #{hunted_sheep_index}")

        print(f'\talive sheep: {alive_sheep}')

        if (self.wait):
            print('Simulation stopped. Press any key to continue')
            getch()

    def __read_from_config(self, config_filename: str):
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
        # move sheep flock 
        for sheep in self.sheep_flock:
            if (sheep is None):
                continue

            sheep.move()

        # move wolf
        hunted_sheep_index, sheep_eaten = self.wolf.move(self.sheep_flock)

        # remove sheep if eaten
        if (sheep_eaten):
            self.sheep_flock[hunted_sheep_index] = None

        return hunted_sheep_index, sheep_eaten

    def __export_animal_locations(self, filename: str, locations: list):
        with open(filename, 'w') as f:
            dump(locations, f, indent=4)

    def __export_sheep_count(self, filename: str, data: list):
        with open(filename, 'w') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['round_no', 'alive_sheep'])
            csv_writer.writerows(data)
