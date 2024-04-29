import logging
import multiprocessing
import os
from NPC import NPC
import json
from generic_automata import Automata

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')


class Environment():
    def get_NPCS(self):
        return self.NPCs_map
    
    def get_NPCS_names(self):
        return self.NPCs_map.keys()
    
    def get_NPC(self, name):
        return self.NPCs_map[name]
    
    def add_NPC(self, name, slider_value=0):
        npc = NPC(name, self, self.get_base_NPC_traits(),self.get_automata_tags(), self.get_automata_text(), self.get_automata_on_transition_actions(), self.get_automata_transitions())
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
        
        

    def get_Current_NPC_traits(self, name):
        # go through the file and get the chosen traits
        try:
            with open(self.NPCs_map[name].file.name, 'r') as f: 
                data = json.load(f)
                # choose the traits from the dictionary
                chosen_traits = data.get(name, {}).get("traits", [])
                return chosen_traits
        except FileNotFoundError:
            logging.warning(f"File {self.NPCs_map[name].file.name} not found")
            return []
        except json.JSONDecodeError:
            logging.warning(f"JSONDecodeError")
            return []

    def get_Current_NPC_Next_Transitions(self, name):
        # go through the file and get next states
        try:
            with open(self.NPCs_map[name].file.name, 'r') as f: 
                data = json.load(f)
                # choose the action from the dictionary
                next_states = data.get(name, {}).get("next_states", [])
                return next_states
        except FileNotFoundError:
            logging.warning(f"File {self.NPCs_map[name].file.name} not found")
            return []
        except json.JSONDecodeError:
            logging.warning(f"JSONDecodeError")
            return []

    def set_Current_NPC_action(self, name, action):
        # go through the file and set the action
        with open(self.NPCs_map[name].file.name, 'r+') as f:
            data = json.load(f)
            npc_data = data.get(name, {})
            npc_data["action"] = action
            data[name] = npc_data
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            f.flush()
            logging.info(f"NPC {name} action set to {action}")
        
    def get_base_NPC_traits(self):
        return self.npc_traits
    
    def get_NPC_actions(self):
        return self.npc_actions
    
    def get_env_machine(self):
        return self.automata
    
    def get_automata_instance(self):
        return self.automata.get_automata_instance()
    
    def get_automata_tags(self):
        return self.automata.get_tags()
    
    def get_automata_text(self):
        return self.automata.get_text()
    
    def get_automata_transitions(self):
        return self.automata.get_transitions()
    
    def get_automata_on_transition_actions(self):
        return self.automata.get_on_transition_actions()
    
    def get_name(self):
        return self.name
        
    def __init__(self, name, npc_traits, npc_actions) -> None:
        # Create a dictionary to store the labels for each NPC and their traits
        self.name = name
        self.NPCs_process_map = {}
        self.NPCs_map = {}
        self.file_names = []
        self.npc_actions = npc_actions
        self.npc_traits = npc_traits
        self.automata = Automata(npc_traits, npc_actions, name)
        logging.info(f"Environment {name} created")
        
        
    
    