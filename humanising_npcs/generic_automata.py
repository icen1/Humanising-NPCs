import logging
import utils


class Automata():
    def __init__(self, npc_traits, environment_traits, name) -> None:
        self.npc_traits = npc_traits
        self.environment_traits = environment_traits

        definition = {
            "states": {
                "Start": {"initial": True},
                "loop": {},
                "End": {"final": True},
            },
            "events": {
                "start_to_loop": [
                    {"from": "Start", "to": "loop"},
                ],
                "loop_to_start": [
                    {"from": "loop", "to": "Start"},
                ],
                "loop_to_end": [
                    {"from": "loop", "to": "End"},
                ],
            },
        }
        logging.info("Start and End states created")
        logging.info("loop to Start and End transitions created")
        
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

        # connect the last middle state to the loop state
        definition["events"][f"middle_state_{counter}_to_loop"] = [{"from": f"middle_state_{counter}", "to": "loop"}]
        # Create the state machine class
        machine = utils.create_machine_class_from_definition(name, definition)
        self.automata = machine()
        
    
    def get_machine(self):
        return self.automata
    
    def get_current_state(self):
        return self.automata.current_state.value
    
    def send_event(self, event):
        self.automata.send(event)
        
    def get_npc_traits(self):
        return self.npc_traits
    
    def get_environment_traits(self):
        return self.environment_traits
    
