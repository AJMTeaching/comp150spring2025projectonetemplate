import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Event, Character, Statistic, EventStatus

class TestEvent(unittest.TestCase):
    """Tests for the Event class."""
    
    def setUp(self):
        """Set up test data before each test."""
        self.event_data = {
            "primary_attribute": "Intelligence",
            "secondary_attribute": "Cunning",
            "prompt_text": "The ancient library contains a book with a complex cipher. How will you decode it?",
            "pass": {
                "message": "Your intelligence allows you to decipher the text, revealing crucial information."
            },
            "fail": {
                "message": "The cipher is too complex, and you leave empty-handed."
            },
            "partial_pass": {
                "message": "Your cunning approach reveals part of the message, though some sections remain indecipherable."
            }
        }
        
        self.event = Event(self.event_data)
        
        # Create a test character
        self.character = Character("Samwell Tarly")
        
        # Create a mock parser
        self.mock_parser = MagicMock()
    
    def test_event_initialization(self):
        """Test that an event is correctly initialized with data."""
        self.assertEqual(self.event.primary_attribute, "Intelligence")
        self.assertEqual(self.event.secondary_attribute, "Cunning")
        self.assertEqual(self.event.prompt_text, self.event_data["prompt_text"])
        self.assertEqual(self.event.pass_message, self.event_data["pass"]["message"])
        self.assertEqual(self.event.fail_message, self.event_data["fail"]["message"])
        self.assertEqual(self.event.partial_pass_message, self.event_data["partial_pass"]["message"])
        self.assertEqual(self.event.status, EventStatus.UNKNOWN)
    
    def test_resolve_choice_primary_attribute(self):
        """Test resolving an event with the primary attribute."""
        # Set up a stat matching the primary attribute
        self.character.intelligence.value = 70
        
        # Resolve choice with primary attribute
        self.event.resolve_choice(self.character, self.character.intelligence)
        
        # Check result is a PASS
        self.assertEqual(self.event.status, EventStatus.PASS)
    
    def test_resolve_choice_secondary_attribute(self):
        """Test resolving an event with the secondary attribute."""
        # Set up a stat matching the secondary attribute
        self.character.cunning.value = 65
        
        # Resolve choice with secondary attribute
        self.event.resolve_choice(self.character, self.character.cunning)
        
        # Check result is a PARTIAL_PASS
        self.assertEqual(self.event.status, EventStatus.PARTIAL_PASS)
    
    def test_resolve_choice_wrong_attribute(self):
        """Test resolving an event with a non-matching attribute."""
        # Use strength which matches neither primary nor secondary
        self.character.strength.value = 80
        
        # Resolve choice with wrong attribute
        self.event.resolve_choice(self.character, self.character.strength)
        
        # Check result is a FAIL
        self.assertEqual(self.event.status, EventStatus.FAIL)
    
    @patch('builtins.print')
    def test_execute_event(self, mock_print):
        """Test executing an event with a party."""
        # Create test party
        party = [self.character]
        
        # Mock parser responses
        self.mock_parser.select_party_member.return_value = self.character
        self.mock_parser.select_stat.return_value = self.character.intelligence
        
        # Execute event
        self.event.execute(party, self.mock_parser)
        
        # Verify method calls
        self.mock_parser.select_party_member.assert_called_once_with(party)
        self.mock_parser.select_stat.assert_called_once_with(self.character)
        
        # Check print was called with prompt_text and pass_message
        mock_print.assert_any_call(self.event_data["prompt_text"])
        mock_print.assert_any_call(self.event_data["pass"]["message"])
        
        # Check final status
        self.assertEqual(self.event.status, EventStatus.PASS)
    
    def test_different_event_types(self):
        """Test events with different attribute combinations."""
        # Test strength/endurance event
        strength_event_data = {
            "primary_attribute": "Strength",
            "secondary_attribute": "Endurance",
            "prompt_text": "A massive boulder blocks the path. Can you move it?",
            "pass": {"message": "With your strength, you push the boulder aside."},
            "fail": {"message": "The boulder is too heavy to move."},
            "partial_pass": {"message": "Your endurance allows you to shift it enough to squeeze by."}
        }
        
        strength_event = Event(strength_event_data)
        
        # Test with primary attribute
        self.character.strength.value = 75
        strength_event.resolve_choice(self.character, self.character.strength)
        self.assertEqual(strength_event.status, EventStatus.PASS)
        
        # Test with secondary attribute
        strength_event.status = EventStatus.UNKNOWN  # Reset status
        self.character.endurance.value = 60
        strength_event.resolve_choice(self.character, self.character.endurance)
        self.assertEqual(strength_event.status, EventStatus.PARTIAL_PASS)

if __name__ == '__main__':
    unittest.main()
