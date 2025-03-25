import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import UserInputParser, Character, Statistic

class TestUserInputParser(unittest.TestCase):
    """Test the UserInputParser class and its methods."""
    
    def setUp(self):
        """Initialize test data before each test."""
        self.parser = UserInputParser()
        
        # Create test characters
        self.character = Character("Cersei")
        self.party = [
            self.character,
            Character("Jaime"),
            Character("Tyrion")
        ]
    
    @patch('builtins.input', return_value="test input")
    def test_parse(self, mock_input):
        """Test parsing user input."""
        result = self.parser.parse("Enter something: ")
        
        # Check that input was called with the prompt
        mock_input.assert_called_once_with("Enter something: ")
        
        # Check that the result is the mock input value
        self.assertEqual(result, "test input")
    
    @patch('builtins.print')
    @patch('builtins.input', return_value="2")
    def test_select_party_member(self, mock_input, mock_print):
        """Test selecting a party member."""
        result = self.parser.select_party_member(self.party)
        
        # Check that the party members were displayed
        mock_print.assert_any_call("Choose a party member:")
        for i, char in enumerate(self.party):
            mock_print.assert_any_call(f"{i + 1}. {char.name}")
        
        # Check that the correct party member was returned
        self.assertEqual(result, self.party[1])  # Index 1 for input "2"
    
    @patch('builtins.print')
    @patch('builtins.input', return_value="3")
    def test_select_stat(self, mock_input, mock_print):
        """Test selecting a character stat."""
        # Set custom values for stats to verify
        self.character.intelligence.value = 85
        self.character.charisma.value = 90
        
        result = self.parser.select_stat(self.character)
        
        # Check that the stats were displayed
        mock_print.assert_any_call(f"Choose a stat for {self.character.name}:")
        stats = self.character.get_stats()
        for i, stat in enumerate(stats):
            mock_print.assert_any_call(f"{i + 1}. {stat.name} ({stat.value})")
        
        # Check that the correct stat was returned (assuming we have 6 stats: strength, intelligence, charisma, stealth, cunning, endurance)
        self.assertEqual(result, stats[2])  # Index 2 for input "3" (charisma)
    
    @patch('builtins.print')
    @patch('builtins.input')
    def test_select_invalid_party_member(self, mock_input, mock_print):
        """Test selecting an invalid party member index."""
        # First try with invalid index, then with valid
        mock_input.side_effect = ["10", "2"]
        
        # This should cause an IndexError which would be caught in a real application
        # For testing, we'll just verify the function tries to access the correct index
        with self.assertRaises(IndexError):
            self.parser.select_party_member(self.party)
    
    @patch('builtins.print')
    @patch('builtins.input')
    def test_select_invalid_stat(self, mock_input, mock_print):
        """Test selecting an invalid stat index."""
        # First try with invalid index, then with valid
        mock_input.side_effect = ["10", "1"]
        
        # This should cause an IndexError which would be caught in a real application
        # For testing, we'll just verify the function tries to access the correct index
        with self.assertRaises(IndexError):
            self.parser.select_stat(self.character)
            
    @patch('builtins.input')
    def test_parse_non_integer(self, mock_input):
        """Test parsing non-integer input for selections."""
        mock_input.return_value = "not an integer"
        
        # This should cause a ValueError which would be caught in a real application
        with self.assertRaises(ValueError):
            self.parser.select_party_member(self.party)

if __name__ == '__main__':
    unittest.main()
