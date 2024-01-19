from typing import Any
from statemachine import StateMachine, State
import logging
import os

def parse_traits(traits=" , "):
# parse string to list of tuples where each tuple is a pair of opposite traits
    traits = traits.split(",")
    traits = [tuple(trait.split("-")) for trait in traits]
    return traits
def parse_environment(environment=" , "):
    # parse string to list of strings where each string is an environment
    environment = environment.split(",")
    return environment


    
# get the traits from an environment variable
traits_env = parse_traits(os.environ.get('HUMANISING_NPCS_TRAITS'))
environment_env = parse_environment(os.environ.get('HUMANISING_NPCS_ENVIRONMENT'))


class Automata(StateMachine):
    traits = traits_env
    environment = environment_env
    Start = State('Start', initial=True)
    loop = State('loop', initial=False)
    End = State('End', initial=False, final=True)
    loop_to_start = loop.to(Start)
    start_to_loop = Start.to(loop)
    loop_to_end = loop.to(End)
    transition_names = ["start_to_loop"]
    logging.info("Start and End states created")
    logging.info("loop to Start and End transitions created")
    
    def __init__(self):
        if not self.check():
            logging.error("Traits or enviroment not set")
        super().__init__()
    
    # get states_storage
    def get_states(self):
        return list(self.states_storage.values())
    
    def get_events(self):
        return self.events
    
    
    
    # check if traits and enviroment are set
    def check(self):
        if self.traits == [(0,0),(0,0)]:
            logging.error("Traits not set")
            return False
        if self.environment == None:
            logging.error("Enviroment not set")
            return False
        return True
    
    # create transition functions
    def create_transition_function(self, from_state, to_state, template=""):
        def on_enter_function():
            logging.info(f"Transition enter on {from_state} created")
        def on_exit_function():
            logging.info(f"Transition exit on {from_state} created")
        
        return on_enter_function, on_exit_function
    
    def get_transitions(self):
        return self.transition_names
    
    def get_traits(self):
        return self.traits
    
    def get_environment(self):
        return self.environment
    
    def graph_png(self, name="state_diagram.png"):
        return self._graph().write_png(f"{name}")
    
    for counter, opposite_traits in enumerate(traits):
        locals()[opposite_traits[0]] = State(name=opposite_traits[0])
        locals()[opposite_traits[1]] = State(name=opposite_traits[1])
        locals()[f"middle_state_{counter}"] = State(name=f"middle_state_{counter}")
        logging.info(f"States {opposite_traits[0]}, {opposite_traits[1]} and middle_state_{counter} created. Counter: {counter}")
        

        if counter == 0:  # If it's the first iteration, create transitions from start state
            locals()[f"start_to_{opposite_traits[0]}"] = locals()['Start'].to(locals()[opposite_traits[0]])
            locals()[f"start_to_{opposite_traits[1]}"] = locals()['Start'].to(locals()[opposite_traits[1]])
            logging.info(f"Start to {opposite_traits[0]} and {opposite_traits[1]} transitions created")
            locals()[f"{opposite_traits[0]}_to_middle_state_{counter}"] = locals()[opposite_traits[0]].to(locals()[f"middle_state_{counter}"])
            locals()[f"{opposite_traits[1]}_to_middle_state_{counter}"] = locals()[opposite_traits[1]].to(locals()[f"middle_state_{counter}"])
            logging.info(f"{opposite_traits[0]} and {opposite_traits[1]} to middle_state_{counter} transitions created")
            transition_names.append(f"start_to_{opposite_traits[0]}")
            transition_names.append(f"start_to_{opposite_traits[1]}")
            transition_names.append(f"{opposite_traits[0]}_to_middle_state_{counter}")
            transition_names.append(f"{opposite_traits[1]}_to_middle_state_{counter}")
            
        else:
            locals()[f"middle_state_{counter-1}_to_{opposite_traits[0]}"] = locals()[f"middle_state_{counter-1}"].to(locals()[opposite_traits[0]])
            locals()[f"middle_state_{counter-1}_to_{opposite_traits[1]}"] = locals()[f"middle_state_{counter-1}"].to(locals()[opposite_traits[1]])
            logging.info(f"middle_state_{counter-1} to {opposite_traits[0]} and {opposite_traits[1]} transitions created")
            locals()[f"{opposite_traits[0]}_to_middle_state_{counter}"] = locals()[opposite_traits[0]].to(locals()[f"middle_state_{counter}"])
            locals()[f"{opposite_traits[1]}_to_middle_state_{counter}"] = locals()[opposite_traits[1]].to(locals()[f"middle_state_{counter}"])
            logging.info(f"{opposite_traits[0]} and {opposite_traits[1]} to middle_state_{counter} transitions created")
            transition_names.append(f"middle_state_{counter-1}_to_{opposite_traits[0]}")
            transition_names.append(f"middle_state_{counter-1}_to_{opposite_traits[1]}")
            transition_names.append(f"{opposite_traits[0]}_to_middle_state_{counter}")
            transition_names.append(f"{opposite_traits[1]}_to_middle_state_{counter}")

    # Last middle state to end
    locals()[f"middle_state_{counter}_to_loop"] = locals()[f"middle_state_{counter}"].to(loop)
    logging.info(f"middle_state_{counter} to End transition created")
    transition_names.append(f"middle_state_{counter}_to_loop")
    transition_names.append("loop_to_start")
    transition_names.append("loop_to_end")
    

    
# def main():
#     # set traits and environment in the environment variables
#     os.environ['HUMANISING_NPCS_TRAITS'] = "diligent-lazy,gregarious-shy,generous-greedy,brave-cowardly"
#     os.environ['HUMANISING_NPCS_ENVIRONMENT'] = "forest,city"
    
#     # print all environment variables
#     print(os.environ)

#     traits = os.getenv('HUMANISING_NPCS_TRAITS')
#     environment = os.getenv('HUMANISING_NPCS_ENVIRONMENT')
#     print(f"Traits: {traits}")
#     print(f"Enviroment: {environment}")
#     # create a state machine
#     sm = Automata()

    
#     # print the state machine
#     sm._graph().write_png('state_diagram.png')
    
# if __name__ == "__main__":
#     main()