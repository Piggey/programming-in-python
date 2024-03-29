from argparse import ArgumentParser

class ArgParser:

    def __init__(self):
        self.parser = ArgumentParser(add_help=True)

    def get_parsed_arguments(self):
        self.__create_args()

        args = self.parser.parse_args()
        return args

    def __create_args(self):
        self.parser.add_argument(
            '-c', '--config',
            help='an auxiliary configuration file',
            action='store',
            nargs=1,
            dest='config',
        )

        self.parser.add_argument(
            '-d', '--dir',
            help='a subdirectory where output files should be placed',
            action='store',
            nargs=1,
            dest='dir'
        )

        self.parser.add_argument(
            '-l', '--log',
            help='whether or not events should be logged and on what level',
            action='store',
            nargs=1,
            dest='log',
            choices=[ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ]
        )

        self.parser.add_argument(
            '-r', '--rounds',
            help='a number of simulated rounds',
            action='store',
            nargs=1,
            dest='rounds',
            type=int
        )

        self.parser.add_argument(
            '-s', '--sheep',
            help='a number of sheep in flock',
            action='store',
            nargs=1,
            dest='sheep',
            type=int
        )

        self.parser.add_argument(
            '-w', '--wait',
            help='whether or not to pause the simulation at the end of each round',
            action='store_true',
            dest='wait'
        )
