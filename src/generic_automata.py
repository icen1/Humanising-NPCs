import logging
import utils
from collections import defaultdict



class Automata():
    def __init__(self, npc_traits, npc_actions, name) -> None:
        self.npc_traits = npc_traits
        self.npc_actions = npc_actions
        self.transitions = {}
        self.tags = {}
        self.text = {}
        self.on_transition_actions = {}

        definition = {
            "states": {
                "Start": {"initial": True},
                "connector": {},
                "End": {"final": True},
            },
            "events": {
            },
        }
        logging.info("Start and End states created")
        logging.info("connector state created")
        
        for counter, opposite_traits in enumerate(self.npc_traits):
            # Create states
            definition["states"][opposite_traits[0]] = {}
            definition["states"][opposite_traits[1]] = {}
            definition["states"][f"middle_state_{counter}"] = {}

            if counter == 0:  # If it's the first iteration, create transitions from start state
                definition["events"][f"start_to_{opposite_traits[0]}"] = [{"from": "Start", "to": opposite_traits[0]}]
                definition["events"][f"start_to_{opposite_traits[1]}"] = [{"from": "Start", "to": opposite_traits[1]}]
                definition["events"][f"{opposite_traits[0]}_to_middle_state_{counter}"] = [{"from": opposite_traits[0], "to": f"middle_state_{counter}"}]
                definition["events"][f"{opposite_traits[1]}_to_middle_state_{counter}"] = [{"from": opposite_traits[1], "to": f"middle_state_{counter}"}]
            else:
                definition["events"][f"middle_state_{counter-1}_to_{opposite_traits[0]}"] = [{"from": f"middle_state_{counter-1}", "to": opposite_traits[0]}]
                definition["events"][f"middle_state_{counter-1}_to_{opposite_traits[1]}"] = [{"from": f"middle_state_{counter-1}", "to": opposite_traits[1]}]
                definition["events"][f"{opposite_traits[0]}_to_middle_state_{counter}"] = [{"from": opposite_traits[0], "to": f"middle_state_{counter}"}]
                definition["events"][f"{opposite_traits[1]}_to_middle_state_{counter}"] = [{"from": opposite_traits[1], "to": f"middle_state_{counter}"}]
        # connect the last middle state to the connector state
        definition["events"][f"middle_state_{counter}_to_connector"] = [{"from": f"middle_state_{counter}", "to": "connector"}]
        counter = 0
        unreachable_states = [] # to connect them to connector later
        reachable_states = ["connector"]
        #TODO: Add the option to have tags for connectors
        for counter, action_data in enumerate(self.npc_actions):
            # create state if it doesn't exist
            if action_data[0] not in definition["states"]:
                definition["states"][action_data[0]] = {}
            if action_data[2] not in definition["states"]:
                definition["states"][action_data[2]] = {}
            # check direction of transition
            if action_data[1] == ">":
                from_state, _, to_state,_,_,_ = action_data
                definition["events"][f"{from_state}_to_{to_state}"] = [{"from": from_state, "to": to_state}]
                self.transitions[f"{from_state}_to_{to_state}"] = [{"from": from_state, "to": to_state}]
                if from_state in reachable_states:
                    if from_state in unreachable_states:
                        unreachable_states.remove(from_state)
                    
                elif from_state not in unreachable_states:
                    unreachable_states.append(from_state)

                reachable_states.append(to_state)
                       
            else:
                to_state, _, from_state,_,_,_ = action_data
                definition["events"][f"{from_state}_to_{to_state}"] = [{"from": from_state, "to": to_state}]
                self.transitions[f"{from_state}_to_{to_state}"] = [{"from": from_state, "to": to_state}]
                
                if from_state == "connector" or from_state in reachable_states:
                    unreachable_states.remove(from_state)
                elif from_state not in unreachable_states:
                    unreachable_states.append(from_state)

                reachable_states.append(to_state)
                
            if action_data[3] is not None:
                self.tags[f"{action_data[0]}_to_{action_data[2]}"] = action_data[3]
            if action_data[4] is not None:
                self.text[f"{action_data[0]}_to_{action_data[2]}"] = action_data[4]
            if action_data[5] is not None:
                self.on_transition_actions[f"{action_data[0]}_to_{action_data[2]}"] = action_data[5]
            # if it is the last state, connect it to the End state
            if counter == len(self.npc_actions)-1:
                if action_data[1] == ">":
                    definition["events"][f"{action_data[2]}_to_End"] = [{"from": action_data[2], "to": "End"}]
                    self.transitions[f"{action_data[2]}_to_End"] = [{"from": action_data[2], "to": "End"}]
                else:
                    definition["events"][f"{action_data[0]}_to_End"] = [{"from": action_data[0], "to": "End"}]
                    self.transitions[f"{action_data[0]}_to_End"] = [{"from": action_data[0], "to": "End"}]
                    
            # connect the connector state to the unreachable states
            for state in unreachable_states:
                definition["events"][f"connector_to_{state}"] = [{"from": "connector", "to": state}]
                self.transitions[f"connector_to_{state}"] = [{"from": "connector", "to": state}]
            
                
            
        
        
        logging.info("States and transitions created")
        
        # Create the state machine class
        self.machine = utils.create_machine_class_from_definition(name, definition)
        
    
    def get_machine(self):
        return self.machine
    
    def get_automata_instance(self):
        return self.machine()
        
    def get_npc_traits(self):
        return self.npc_traits
    
    def get_npc_actions(self):
        return self.npc_actions
    
    def get_tags(self):
        return self.tags
    
    def get_text(self):
        return self.text
    
    def get_on_transition_actions(self):
        return self.on_transition_actions
    
    def get_transitions(self):
        return self.transitions
