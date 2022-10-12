from Simulation import Simulation
from ArgParser import ArgParser


def main():
    # get and parse arguments
    arg_parser = ArgParser()
    args = arg_parser.get_parsed_arguments()

    sim = Simulation(args)
    sim.start()

if (__name__ == '__main__'):
    main()