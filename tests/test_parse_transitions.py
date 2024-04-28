import unittest
import os
import sys

# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(f"{parent_dir}/src")

import utils

class TestParseTransitions(unittest.TestCase):
    def test_parse_transitions(self):
        # Test with a single transition
        transitions = "trait1>[tag]trait2{text}(+var)"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text", ["+var"])])

        # Test with multiple transitions
        transitions = "trait1>[tag]trait2{text}(+var),trait3<trait4(-var)"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text", ["+var"]), ("trait3", "<", "trait4", None, None, ["-var"])])

        # Test with optional tag, text, and variables
        transitions = "trait1>trait2"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", None, None, None)])

        # Test with whitespace
        transitions = " trait1 > [tag] trait2 {text} (+var) "
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text", ["+var"])])

        # Test with invalid direction
        transitions = "trait1=trait2"
        with self.assertRaises(ValueError):
            utils.parse_transitions(transitions)

        # Test with multiple variables
        transitions = "trait1>[tag]trait2{text}(+var; -var2),trait3<trait4(-var; +var2; -var3)"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [("trait1", ">", "trait2", "tag", "text", ["+var", "-var2"]), ("trait3", "<", "trait4", None, None, ["-var", "+var2", "-var3"])])
        
        transitions = "connector>no_groceries,no_groceries>[diligent]groceries{Get food}(+hunger;-money),groceries>meat{protein source}(+food;-money),groceries>veg{vitamin source}(+vitamins;-money),groceries>fruits{fiber source}(+fiber;-money),meat>[generous]steak{tasty meat}(+satisfaction;-money),veg>[greedy]salad{healthy meal}(+nutrition;-money),fruits>[healthy]apple{delicious fruit}(+happiness;-money),connector>[diligent]work{earn money}(+money),work>connector,salad>eat,steak>eat,apple>eat,work>work(+money),connector>[money]clothes(+tshirt),clothes>connector"
        result = utils.parse_transitions(transitions)
        self.assertEqual(result, [('connector', '>', 'no_groceries', None, None, None), ('no_groceries', '>', 'groceries', 'diligent', 'Getfood', ['+hunger', '-money']), ('groceries', '>', 'meat', None, 'proteinsource', ['+food', '-money']), ('groceries', '>', 'veg', None, 'vitaminsource', ['+vitamins', '-money']), ('groceries', '>', 'fruits', None, 'fibersource', ['+fiber', '-money']), ('meat', '>', 'steak', 'generous', 'tastymeat', ['+satisfaction', '-money']), ('veg', '>', 'salad', 'greedy', 'healthymeal', ['+nutrition', '-money']), ('fruits', '>', 'apple', 'healthy', 'deliciousfruit', ['+happiness', '-money']), ('connector', '>', 'work', 'diligent', 'earnmoney', ['+money']), ('work', '>', 'connector', None, None, None), ('salad', '>', 'eat', None, None, None), ('steak', '>', 'eat', None, None, None), ('apple', '>', 'eat', None, None, None), ('work', '>', 'work', None, None, ['+money']), ('connector', '>', 'clothes', 'money', None, ['+tshirt']), ('clothes', '>', 'connector', None, None, None)])

if __name__ == '__main__':
    unittest.main()