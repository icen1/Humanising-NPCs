from statemachine.factory import StateMachineMetaclass
from statemachine.state import State
from statemachine.statemachine import StateMachine


def test_create_machine_class_from_definition(name: str, definition: dict):
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

class TestWalker():
    def __init__(self, current_value, environment, name) -> None:
        self.current_value = current_value
        self.environment = environment
        self.name = name
        
    def test_walk(self, state):
        self.environment.test_do_walk(state)
        self.current_value = self.environment.test_get_current_state()
        
    def test_get_current_value(self):
        try:
            return self.current_value.name
        except AttributeError:
            return self.current_value
        
        
        
class TestEnvironment():
    def __init__(self, name, definition) -> None:
        self.automata = test_create_machine_class_from_definition(name, definition)() # extra () to create the automata and not its metaclass
        self.name = name
    
    def test_do_walk(self, state):
        self.automata.send(state)
    
    def test_get_current_state(self):
        return self.automata.current_state
        
if __name__ == "__main__":
    definition = {
            "states": {
                "green": {"initial": True},
                "yellow": {},
                "red": {},
            },
            "events": {
                "change": [
                    {"from": "green", "to": "yellow"},
                    {"from": "yellow", "to": "red"},
                    {"from": "red", "to": "green"},
                ]
            },
        }
    env = TestEnvironment("Traffic Light", definition)
    walker = TestWalker(0, env, "walker1")
    walker1 = TestWalker(0, env, "walker2")
    walker.test_walk("change")
    assert walker.test_get_current_value() == "Yellow" # walker reads the current state from the environment and changes its own state
    assert walker1.test_get_current_value() == 0 # walker1 DOES NOT read the current state as we did not use test_walk
    walker1.test_walk("change")
    assert walker1.test_get_current_value() == "Yellow" # Breaks here is the environment is shared between walkers and walker1 reads the current state
                                                        # which was changed by walker to Yellow and then walker1 changes it to Red
    
    
        