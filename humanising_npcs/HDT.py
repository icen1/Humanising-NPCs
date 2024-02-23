from typing import Any
import logging
from environment import Environment
from NPC import NPC
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')

class HDT():
    environments_traits_map = {}
    
    
    def __init__(self) -> None:
        pass
    def add_environment(self, environment_name, environment_traits, npc_traits):
        env = Environment(environment_name, environment_traits, npc_traits)
        self.environments_traits_map[environment_name] = env
    
    def remove_environment(self, environment_name):
        self.environments_traits_map.pop(environment_name)
    
    def get_environments(self):
        return self.environments_traits_map
    
    def get_environment(self, environment_name):
        return self.environments_traits_map[environment_name]
    
    def get_environment_traits(self, environment_name):
        return self.environments_traits_map[environment_name].env_traits
    
    def get_environment_names(self):
        return self.environments_traits_map.keys()
    
    def get_environment_NPCs(self, environment_name):
        return self.environments_traits_map[environment_name].get_NPCS()
    
    def get_environment_NPCs_names(self, environment_name):
        return self.environments_traits_map[environment_name].get_NPCS_names()