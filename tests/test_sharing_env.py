import unittest
from statemachine.factory import StateMachineMetaclass
from statemachine.state import State
from statemachine.statemachine import StateMachine
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

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
        self.automata = utils.create_machine_class_from_definition(name, definition)()
        self.name = name
    
    def test_do_walk(self, state):
        self.automata.send(state)
    
    def test_get_current_state(self):
        return self.automata.current_state
        
class TestStateMachine(unittest.TestCase):
    def setUp(self):
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
        self.env = TestEnvironment("Traffic Light", definition)
        self.walker = TestWalker(0, self.env, "walker1")
        self.walker1 = TestWalker(0, self.env, "walker2")

    def test_walkers(self):
        self.walker.test_walk("change")
        self.assertEqual(self.walker.test_get_current_value(), "Yellow")
        self.assertEqual(self.walker1.test_get_current_value(), 0)
        self.walker1.test_walk("change")
        self.assertNotEqual(self.walker1.test_get_current_value(), "Yellow")
if __name__ == "__main__":
    unittest.main()