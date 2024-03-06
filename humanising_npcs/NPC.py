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
        # draw graph of the automata
        # self.npc_automata._graph().write_png(f"{self.environment.name}_{self.name}.png")
        
        
        logging.info(f"NPC started")
        logging.info(f"Traits: {self.traits}")
        logging.info(f"Actions: {self.tags}")
        # make chosen traits an array of zeros equal to the number of opposite tuples in npc.get_traits()
        self.chosen_traits = [""]*len(self.traits)
        mode = -1 if slider_value > 0 else 1
        counter = 0
        for counter, opposite_traits in enumerate(self.traits):
            if counter == 0:
                if slider_value + mode * random.uniform(0, 1) > 0:
                    self.chosen_traits[counter] = opposite_traits[0]
                    logging.info(f"Trait {opposite_traits[0]} chosen, chosen_traits: {self.chosen_traits}")
                    self.npc_automata.send(f"start_to_{opposite_traits[0]}")
                    self.npc_automata.send(f"{opposite_traits[0]}_to_middle_state_{counter}")
                else:
                    self.chosen_traits[counter] = opposite_traits[1]
                    logging.info(f"Trait {opposite_traits[1]} chosen, chosen_traits: {self.chosen_traits}")
                    self.npc_automata.send(f"start_to_{opposite_traits[1]}")
                    self.npc_automata.send(f"{opposite_traits[1]}_to_middle_state_{counter}")
            else:
                if slider_value+mode*random.uniform(0,1) > 0:
                    self.chosen_traits[counter] = opposite_traits[0]
                    logging.info(f"Trait {opposite_traits[0]} chosen, chosen_traits: {self.chosen_traits}")
                    self.npc_automata.send(f"middle_state_{counter-1}_to_{opposite_traits[0]}")
                    self.npc_automata.send(f"{opposite_traits[0]}_to_middle_state_{counter}")
                else:
                    self.chosen_traits[counter] = opposite_traits[1]
                    logging.info(f"Trait {opposite_traits[1]} chosen, chosen_traits: {self.chosen_traits}")
                    self.npc_automata.send(f"middle_state_{counter-1}_to_{opposite_traits[1]}")
                    self.npc_automata.send(f"{opposite_traits[1]}_to_middle_state_{counter}")
        self.npc_automata.send(f"middle_state_{counter}_to_connector")
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
            data[self.name] = {
                "traits": self.chosen_traits,
                "action": "",
                "next_states": self.get_next_state_values()
            }

            # Write updated data back to file
            f.seek(0)  # reset file pointer to start
            logging.info(f"{self.name} traits: {data[self.name]}")
            f.truncate()  # remove existing file content
            json.dump(data, f)
            logging.info(f"File data: {data}")
            f.flush()

        while not self.kill:
            # Open the file and load the data
            with open(self.file.name, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                    logging.warning("JSON Decode error, set data to {}")

                # Get the next action for this NPC
                npc_data = data.get(self.name, {})
                next_action = npc_data.get("action")
            # If the next action is valid and either it has no tag or its tag is in the chosen traits, perform it
            if next_action in [action for _,action in self.get_next_state_values()] and (next_action not in self.tags.keys() or self.tags[next_action] in self.chosen_traits):
                if next_action in self.on_transition_actions.keys():
                    # go through the list of actions and perform them
                    for action in self.on_transition_actions[next_action]:
                        # action is a string, check if the first character is a + or a -
                        if action[0] == "+":
                            if action[1:] not in self.chosen_traits:
                                self.chosen_traits.append(action[1:])
                        elif action[0] == "-":
                            if action[1:] in self.chosen_traits:
                                self.chosen_traits.remove(action[1:])
                self.npc_automata.send(next_action)
            
                
                # change next_states in json file
                with open(self.file.name, 'r+') as f:
                    data = json.load(f)
                    npc_data = data.get(self.name, {})
                    next_states = self.get_next_state_values()
                    npc_data["next_states"] = next_states
                    data[self.name] = npc_data
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f)
                    f.flush()
                
                # check if the NPC has reached the end state
                if self.npc_automata.current_state.value == "End":
                    logging.info(f"NPC {self.name} reached the end state")
                    self.stop()
                    break
                
            else:
                # If the next action is not valid or its tag is not in the chosen traits, wait for a bit and check again
                time.sleep(1)
            
    def stop(self):
        self.kill = True
        self.environment.remove_NPC(self.name)
        self.file.close()
            
        logging.info(f"NPC stopped")
        
    def __init__(self, name, environment, traits, tags, text, on_transition_actions, transitions) -> None:
        self.chosen_traits = []
        self.name = name
        self.environment = environment
        self.kill = False
        self.file = tempfile.NamedTemporaryFile(prefix=f"environment_{environment.name}_{self.name}_", suffix=".json", delete=False)
        self.traits = traits
        self.tags = tags
        self.transition_text = text
        self.on_transition_actions = on_transition_actions
        self.state_transitions = transitions
        self.npc_automata = environment.get_automata_instance()
        logging.info(f"NPC {name} created")
        
    def get_environment(self):
        return self.environment
    
    def get_traits(self):  
        return self.traits
    
    def get_next_state_values(self):
        # look up all the transitions from the current state and return the next possible states
        current_state = self.npc_automata.current_state.value
        next_states = []
        for transition_value, event_name in self.state_transitions.items():
            transition_name = event_name[0]["from"] + "_to_" + event_name[0]["to"]
            if event_name[0]["from"] == current_state:
                if (transition_name not in self.tags.keys()) or (transition_name in self.tags.keys() and self.tags[transition_name] in self.chosen_traits):
                    next_states.append((event_name[0]["to"], transition_value))
        return next_states
        
    
    