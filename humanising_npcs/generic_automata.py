from typing import Any
from statemachine import StateMachine, State
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='w')

class generic_automata(StateMachine):
    traits = [("diligent","lazy"),("gregarious","shy")]
    environment = ["forest","city"]
    Start = State('Start', initial=True)
    loop = State('loop', initial=False)
    End = State('End', initial=False, final=True)
    loop_to_start = loop.to(Start)
    start_to_loop = Start.to(loop)
    loop_to_end = loop.to(End)
    states_storage = {}
    states_storage['Start'] = Start
    states_storage['End'] = End
    states_storage['loop'] = loop
    logging.info("Start and End states created")
    logging.info("loop to Start and End transitions created")
    
    
    
    def __init__(self, traits, environment):
        self.traits = traits
        self.environment = environment
        if not self.check():
            logging.error("Traits or enviroment not set")
        logging.info(f"Traits: {traits}")
        logging.info(f"Enviroment: {environment}")
        self.states_map = self.states_storage
        super().__init__()
    
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
            
        else:
            locals()[f"middle_state_{counter-1}_to_{opposite_traits[0]}"] = locals()[f"middle_state_{counter-1}"].to(locals()[opposite_traits[0]])
            locals()[f"middle_state_{counter-1}_to_{opposite_traits[1]}"] = locals()[f"middle_state_{counter-1}"].to(locals()[opposite_traits[1]])
            logging.info(f"middle_state_{counter-1} to {opposite_traits[0]} and {opposite_traits[1]} transitions created")
            locals()[f"{opposite_traits[0]}_to_middle_state_{counter}"] = locals()[opposite_traits[0]].to(locals()[f"middle_state_{counter}"])
            locals()[f"{opposite_traits[1]}_to_middle_state_{counter}"] = locals()[opposite_traits[1]].to(locals()[f"middle_state_{counter}"])
            logging.info(f"{opposite_traits[0]} and {opposite_traits[1]} to middle_state_{counter} transitions created")

    # Last middle state to end
    locals()[f"middle_state_{counter}_to_end"] = locals()[f"middle_state_{counter}"].to(loop)
    logging.info(f"middle_state_{counter} to End transition created")
    


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

    
def main():
    # create a state machine
    sm = generic_automata([("diligent","lazy"),("gregarious","shy"),("generous","greedy"),("brave","cowardly")], ["forest","city"])

    
    # print the state machine
    print("Hi")
    sm._graph().write_png('state_diagram.png')
    
if __name__ == "__main__":
    main()