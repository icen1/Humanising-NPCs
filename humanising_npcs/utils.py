import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')


def parse_traits(traits=" , "):
# parse string to list of tuples where each tuple is a pair of opposite traits
    traits = traits.split(",")
    traits = [tuple(trait.split("-")) for trait in traits]
    return traits
def parse_environment(environment=" , "):
    # parse string to list of strings where each string is an environment
    environment = environment.split(",")
    return environment