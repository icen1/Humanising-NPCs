import logging
import tempfile
from generic_automata import Automata
import random
import time
import json
from multiprocessing import Lock
from multiprocessing.process import AuthenticationString

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')

class NPC():
    # start a different thread for the NPC with the traits in the environment variable
    def start(self, slider_value=0):
        logging.info(f"NPC started")
        npc = Automata()
        logging.info(f"Traits: {npc.get_traits()}")
        logging.info(f"Environment: {npc.get_environment()}")
        logging.info(f"Transition names: {npc.get_transitions()}")
        self.environment = npc.get_environment()
        # make chosen traits an array of zeros equal to the number of opposite tuples in npc.get_traits()
        self.chosen_traits = [""]*len(npc.get_traits())
        mode = -1 if slider_value > 0 else 1
        while not self.kill:
            counter = 0
            for counter, opposite_traits in enumerate(npc.get_traits()):
                if counter == 0:
                    if slider_value + mode * random.uniform(0, 1) > 0:
                        self.chosen_traits[counter] = opposite_traits[0]
                        logging.info(f"Trait {opposite_traits[0]} chosen, chosen_traits: {self.chosen_traits}")
                        npc.send(f"start_to_{opposite_traits[0]}")
                        npc.send(f"{opposite_traits[0]}_to_middle_state_{counter}")
                    else:
                        self.chosen_traits[counter] = opposite_traits[1]
                        logging.info(f"Trait {opposite_traits[1]} chosen, chosen_traits: {self.chosen_traits}")
                        npc.send(f"start_to_{opposite_traits[1]}")
                        npc.send(f"{opposite_traits[1]}_to_middle_state_{counter}")
                else:
                    if slider_value+mode*random.uniform(0,1) > 0:
                        self.chosen_traits[counter] = opposite_traits[0]
                        logging.info(f"Trait {opposite_traits[0]} chosen, chosen_traits: {self.chosen_traits}")
                        npc.send(f"middle_state_{counter-1}_to_{opposite_traits[0]}")
                        npc.send(f"{opposite_traits[0]}_to_middle_state_{counter}")
                    else:
                        self.chosen_traits[counter] = opposite_traits[1]
                        logging.info(f"Trait {opposite_traits[1]} chosen, chosen_traits: {self.chosen_traits}")
                        npc.send(f"middle_state_{counter-1}_to_{opposite_traits[1]}")
                        npc.send(f"{opposite_traits[1]}_to_middle_state_{counter}")
            npc.send(f"middle_state_{counter}_to_loop")
            # open the file and write the chosen traits to it as a json
            with open(self.file.name, 'r+') as f:
                # Load existing data
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                    logging.warning("JSON Decode error, set data to \{\}")

                logging.info(f"File data before truncating: {data}")
                # Update data
                data[self.name] = self.chosen_traits

                # Write updated data back to file
                f.seek(0)  # reset file pointer to start
                logging.info(f"{self.name} traits: {data[self.name]}")
                f.truncate()  # remove existing file content
                json.dump(data, f)
                logging.info(f"File data before truncating: {data}")
                f.flush()


            if not self.kill:
                npc.send('loop_to_start')
            else:
                npc.send('loop_to_end')
                break
            
    def stop(self):
        self.kill = True
        # remove the NPC from the environment by looking up the NPC in the json file and removing the entry
        with open(self.file.name, 'r+') as f:
            data = json.load(f)
            data.pop(self.name, None)  # Use None as default to avoid KeyError if the name is not found

            # Write the updated data back to the file
            f.seek(0)  # reset file pointer to start
            f.truncate()  # remove existing file content
            json.dump(data, f)
            f.flush()
        logging.info(f"NPC stopped")
        
    #TODO: dysfunctional
    def get_traits(self):
        return self.chosen_traits
        
    def __init__(self, name, environment) -> None:
        self.chosen_traits = []
        self.name = name
        self.environment = environment
        self.kill = False
        self.file = tempfile.NamedTemporaryFile(prefix=f"environment_{environment.name}_{self.name}_", suffix=".json", delete=False)

        logging.info(f"NPC {name} created")
        
    def get_environment(self):
        return self.environment
    
    #TODO: dysfunctional
    def get_chosen_traits(self):
        logging.info(f"get_chosen_traits called, chosen_traits: {self.chosen_traits}")
        return self.chosen_traits
    
    # def __getstate__(self):
    #     """called when pickling - this hack allows subprocesses to 
    #         be spawned without the AuthenticationString raising an error"""
    #     state = self.__dict__.copy()
    #     conf = state['_config']
    #     if 'authkey' in conf: 
    #         #del conf['authkey']
    #         conf['authkey'] = bytes(conf['authkey'])
    #     return state

    # def __setstate__(self, state):
    #     """for unpickling"""
    #     state['_config']['authkey'] = AuthenticationString(state['_config']['authkey'])
    #     self.__dict__.update(state)
        
        
        
        
    
    