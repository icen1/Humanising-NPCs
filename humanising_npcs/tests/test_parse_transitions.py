import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils
import unittest

class TestParseTransitions(unittest.TestCase):
    def test_parse_transitions(self):
        # Test with a single transition
        transitions = "trait1>[tag]trait2{text}"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text")])

        # Test with multiple transitions
        transitions = "trait1>[tag]trait2{text},trait3<trait4"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text"), ("trait3", "<", "trait4", None, None)])

        # Test with optional tag and text
        transitions = "trait1>trait2"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", None, None)])

        # Test with whitespace
        transitions = " trait1 > [tag] trait2 {text} "
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text")])

        # Test with invalid direction
        transitions = "trait1=trait2"
        with self.assertRaises(ValueError):
            utils.parse_transitions(transitions)

if __name__ == '__main__':
    unittest.main()