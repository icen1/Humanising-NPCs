from typing import Any
from statemachine import StateMachine, State
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='w')

class HDT(StateMachine):
    traits = [("diligent","lazy"),("gregarious","shy")]
    environment = ["forest","city"]
    Start = State('Start', initial=True)
    before_end = State('End', initial=False, final=True)


    
def main():
    # create a state machine
    sm = HDT([("diligent","lazy"),("gregarious","shy"),("generous","greedy"),("brave","cowardly")], ["forest","city"])

    
    # print the state machine
    print("Hi")
    sm._graph().write_png('state_diagram.png')
    
if __name__ == "__main__":
    main()