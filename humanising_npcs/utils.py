import logging
from statemachine.factory import StateMachineMetaclass
from statemachine.state import State
from statemachine.statemachine import StateMachine


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO, filename='log.log',filemode='a')


def parse_traits(traits=" , "):
    # parse string to list of tuples where each tuple is a pair of opposite traits
    traits = traits.split(",")
    traits = [tuple(trait.strip() for trait in trait_pair.split("-")) for trait_pair in traits]
    return traits

def parse_environment(environment=" , "):
    # parse string to list of strings where each string is an environment
    environment = [env.strip() for env in environment.split(",")]
    return environment

def parse_transitions(transitions=" , "):
    """
    Transitions are in the form of a string with the following format:
        "trait1>[tag]trait2{text}(+var)" or "trait1<[tag]trait2{text}(+var;-var)"
        Tag and text are optional
        To separate transitions use a comma
    """

    transitions = transitions.split(",")
    # parse each transition
    for counter, transition in enumerate(transitions):
        # remove spaces
        transition = transition.replace(" ", "")
        # get the direction of the transition
        if ">" in transition:
            direction = ">"
        elif "<" in transition:
            direction = "<"
        else:
            logging.error(f"Invalid transition direction in transition {counter+1}")
            raise ValueError(f"Invalid transition direction in transition {counter+1}")
        # get the tag and text of the transition
        try:
            tag = transition[transition.index("[")+1:transition.index("]")]
        except ValueError:
            tag = None

        try:
            text = transition[transition.index("{")+1:transition.index("}")]
        except ValueError:
            text = None
        # get the variables involved in the transition
        try:
            variables = transition[transition.index("(")+1:transition.index(")")]
            variables = variables.split(";")
        except ValueError:
            variables = None
        # get the traits involved in the transition
        trait1 = transition[:transition.index(direction)]
        if "[" in transition and "{" in transition:
            trait2 = transition[transition.index(']')+1:transition.index("{")]
        elif "[" in transition:
            trait2 = transition[transition.index(']')+1:]
        elif "{" in transition:
            trait2 = transition[transition.index(direction)+1:transition.index("{")]
        elif "(" in transition:
            trait2 = transition[transition.index(direction)+1:transition.index("(")]
        else:
            trait2 = transition[transition.index(direction)+1:]
        transitions[counter] = (trait1, direction, trait2, tag, text, variables)
    return transitions
    

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