from Simulation import Simulation
from ArgParser import ArgParser


def main():
    # get and parse arguments
    arg_parser = ArgParser()
    args = arg_parser.get_parsed_arguments()

    print(args)

    #sim = Simulation(args)
    #sim.run()


if (__name__ == '__main__'):
    main()