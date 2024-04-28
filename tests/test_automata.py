import unittest
import os
import sys

# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(f"{parent_dir}/src")

# Now Python should be able to find the generic_automata module
from generic_automata import Automata

class TestAutomata(unittest.TestCase):

    def setUp(self):
        # Initialize the Automata object with sample data for testing
        npc_traits = [("Trait1", "Trait2"), ("Trait3", "Trait4")]
        npc_actions = [("connector", ">", "Action1", None, None, "+var1"),
                       ("Action1", ">", "Action2", "tag1", "text1","+2var2,-var1"),
                       ("Action2", "<", "Action3", "tag2", "text2","-var2,-var3")]
        name = "TestAutomata"
        self.automata = Automata(npc_traits, npc_actions, name)

    def test_get_machine(self):
        machine = self.automata.get_machine()
        self.assertIsNotNone(machine)

    def test_get_automata_instance(self):
        automata_instance = self.automata.get_automata_instance()
        self.assertIsNotNone(automata_instance)

    def test_get_npc_traits(self):
        traits = self.automata.get_npc_traits()
        self.assertEqual(traits, [("Trait1", "Trait2"), ("Trait3", "Trait4")])

    def test_get_npc_actions(self):
        actions = self.automata.get_npc_actions()
        self.assertEqual(actions, [("connector", ">", "Action1", None, None, "+var1"),
                                   ("Action1", ">", "Action2", "tag1", "text1", "+2var2,-var1"),
                                   ("Action2", "<", "Action3", "tag2", "text2", "-var2,-var3")])


    def test_get_tags(self):
        tags = self.automata.get_tags()
        self.assertEqual(tags, {"Action1_to_Action2": "tag1", "Action2_to_Action3": "tag2"})

    def test_get_text(self):
        text = self.automata.get_text()
        self.assertEqual(text, {"Action1_to_Action2": "text1", "Action2_to_Action3": "text2"})


    def test_get_transitions(self):
        transitions = self.automata.get_transitions()
        expected_transitions = {
            "connector_to_Action1": [{"from": "connector", "to": "Action1"}],
            "Action1_to_Action2": [{"from": "Action1", "to": "Action2"}],
            "Action3_to_Action2": [{"from": "Action3", "to": "Action2"}],
            "Action2_to_End": [{"from": "Action2", "to": "End"}],
            "connector_to_Action3": [{"from": "connector", "to": "Action3"}],
        }
        self.assertEqual(transitions, expected_transitions)

    def test_on_transition_actions(self):
        on_transition_actions = self.automata.get_on_transition_actions()
        expected_on_transition_actions = {
            "connector_to_Action1": ["+var1"],
            "Action1_to_Action2": ["+2var2", "-var1"],
            "Action2_to_Action3": ["-var2", "-var3"],
        }
        self.assertEqual(on_transition_actions, expected_on_transition_actions)

if __name__ == '__main__':
    unittest.main()