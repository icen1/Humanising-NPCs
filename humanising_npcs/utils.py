import logging
from statemachine.factory import StateMachineMetaclass
from statemachine.state import State
from statemachine.statemachine import StateMachine


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')


def parse_traits(traits=" , "):
# parse string to list of tuples where each tuple is a pair of opposite traits
    traits = traits.split(",")
    traits = [tuple(trait.split("-")) for trait in traits]
    return traits
def parse_environment(environment=" , "):
    # parse string to list of strings where each string is an environment
    environment = environment.split(",")
    return environment

def create_machine_class_from_definition(name: str, definition: dict):
    states_instances = {
        state_id: State(**state_kwargs)
        for state_id, state_kwargs in definition["states"].items()
    }

    events = {}
    for event_name, transitions in definition["events"].items():
        for transition_data in transitions:
            source = states_instances[transition_data["from"]]
            target = states_instances[transition_data["to"]]

            transition = source.to(target, event=event_name)

            if event_name in events:
                events[event_name] |= transition
            else:
                events[event_name] = transition

    attrs_mapper = {**states_instances, **events}

    return StateMachineMetaclass(name, (StateMachine,), attrs_mapper)