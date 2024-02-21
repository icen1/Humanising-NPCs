import logging
import multiprocessing
import os
import tempfile
from NPC import NPC
import utils
import json

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')


class Environment():
    def get_NPCS(self):
        return self.NPCs_map
    
    def get_NPCS_names(self):
        return self.NPCs_map.keys()
    
    def get_NPC(self, name):
        return self.NPCs_map[name]
    
    def add_NPC(self, name, slider_value=0):
        npc = NPC(name, self)
        self.NPCs_map[name] = npc
        # start a subprocess for the NPC
        p = multiprocessing.Process(target=npc.start, args=(slider_value,))
        p.start()
        self.NPCs_process_map[name] = p
        logging.info(f"NPC {name} added to environment with processid: {p.pid} and parent processid: {os.getpid()}")
        
        
    
    def remove_NPC(self, name):
        # kill the subprocess for the NPC
        self.NPCs_map[name].stop()
        p = self.NPCs_process_map[name]
        p.terminate()
        p.join()
        self.NPCs_process_map.pop(name)
        self.NPCs_map.pop(name)
        logging.info(f"NPC {name} removed from environment with processid: {p.pid} and parent processid: {os.getpid()}")

    def get_NPC_traits(self, name):
        # go through the file and get the chosen traits
        try:
            with open(self.NPCs_map[name].file.name, 'r') as f: #TODO NPC_map may not contain info needed
                data = json.load(f)
                # choose the only key in the dictionary
                chosen_traits = data[list(data.keys())[0]]
                return chosen_traits
        except FileNotFoundError:
            logging.warning(f"File {self.NPCs_map[name].file.name} not found")
            return []
        except json.JSONDecodeError:
            logging.warning(f"JSONDecodeError")
            return []

    
    def get_name(self):
        return self.name
        
    def __init__(self) -> None:
        self.env_traits = utils.parse_environment(os.environ.get('HUMANISING_NPCS_ENVIRONMENT'))
        
    def __init__(self, name) -> None:
        self.env_traits = utils.parse_environment(os.environ.get('HUMANISING_NPCS_ENVIRONMENT'))
        # Create a dictionary to store the labels for each NPC and their traits
        self.name = name
        self.NPCs_process_map = {}
        self.NPCs_map = {}
        self.file_names = []
        logging.info(f"Environment {name} created")
        
    # def __init__(self, name) -> None:
    #     self.env_traits = utils.parse_environment(os.environ.get('HUMANISING_NPCS_ENVIRONMENT'))
    #     # Create a dictionary to store the labels for each NPC and their traits
    #     self.name = name
    #     self.NPCs_process_map = {}
    #     self.NPCs_map = {}
    #     self.file_names = file_names
    #     logging.info(f"Environment {name} created")
        
        
    
    