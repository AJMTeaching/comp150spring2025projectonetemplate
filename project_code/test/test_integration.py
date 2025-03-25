import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import (
    Character, Location, Event, TravelSystem, Game, UserInputParser, 
    load_events_from_json, load_locations, start_game
)

class TestIntegration(unittest.TestCase):
    """Integration tests for the game components working together."""
    
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch.object(Game, 'start')
    def test_start_game(self, mock_game_start, mock_json_load, mock_file_open, mock_listdir, mock_exists):
        """Test the entire game startup process."""
        # Set up mocks for file operations
        mock_exists.return_value = True
        mock_listdir.side_effect = [
            ['winterfell.json', 'kings_landing.json'],  # Location directory
            ['winterfell_to_kings_landing.json']        # Travel events directory
        ]
        
        # Create mock event data for locations
        winterfell_events = [
            {
                "primary_attribute": "Intelligence",
                "secondary_attribute": "Stealth",
                "prompt_text": "Winterfell event",
                "pass": {"message": "Pass message"},
                "fail": {"message": "Fail message"},
                "partial_pass": {"message": "Partial pass message"}
            }
        ]
        
        kings_landing_events = [
            {
                "primary_attribute": "Charisma",
                "secondary_attribute": "Cunning",
                "prompt_text": "King's Landing event",
                "pass": {"message": "Pass message"},
                "fail": {"message": "Fail message"},
                "partial_pass": {"message": "Partial pass message"}
            }
        ]
        
        # Create mock travel event data
        travel_events = [
            {
                "from_location": "winterfell",
                "to_location": "kings_landing",
                "primary_attribute": "Endurance",
                "secondary_attribute": "Strength",
                "prompt_text": "Travel event",
                "pass": {"message": "Pass message"},
                "fail": {"message": "Fail message"},
                "partial_pass": {"message": "Partial pass message"}
            }
        ]
        
        # Set up json.load to return different data for different files
        mock_json_load.side_effect = [winterfell_events, kings_landing_events, travel_events]
        
        # Call the function to start the game
        with patch('builtins.print'):  # Suppress print output
            start_game()
        
        # Check that Game.start was called
        mock_game_start.assert_called_once()
    
    @patch('builtins.print')
    def test_character_event_interaction(self, mock_print):
        """Test character interaction with an event."""
        # Create character with specific stats
        character = Character("Tyrion")
        character.intelligence.value = 85
        character.cunning.value = 80
        
        # Create an event
        event_data = {
            "primary_attribute": "Intelligence",
            "secondary_attribute": "Cunning",
            "prompt_text": "You need to solve a complex puzzle.",
            "pass": {"message": "Your intelligence helps you solve it easily."},
            "fail": {"message": "You can't figure out the puzzle."},
            "partial_pass": {"message": "Your cunning gives you a partial solution."}
        }
        event = Event(event_data)
        
        # Test primary attribute success
        event.resolve_choice(character, character.intelligence)
        mock_print.assert_called_with("Your intelligence helps you solve it easily.")
        
        # Test secondary attribute partial success
        event.resolve_choice(character, character.cunning)
        mock_print.assert_called_with("Your cunning gives you a partial solution.")
        
        # Test failure with wrong attribute
        event.resolve_choice(character, character.strength)
        mock_print.assert_called_with("You can't figure out the puzzle.")
    
    @patch('builtins.print')
    @patch('builtins.input')
    def test_game_location_exploration_cycle(self, mock_input, mock_print):
        """Test a full cycle of location exploration in the game."""
        # Create a minimal game setup
        parser = UserInputParser()
        characters = [Character("Test Character")]
        
        # Create a location with an event
        location_events = [
            Event({
                "primary_attribute": "Strength",
                "secondary_attribute": "Endurance",
                "prompt_text": "A challenge appears!",
                "pass": {"message": "Success!"},
                "fail": {"message": "Failure!"},
                "partial_pass": {"message": "Partial success!"}
            })
        ]
        locations = {
            "test_location": Location("test_location", "Test Location", location_events)
        }
        
        # Create travel system (minimal functionality needed)
        travel_system = MagicMock(spec=TravelSystem)
        travel_system.get_available_destinations.return_value = []
        
        # Set up the game
        game = Game(parser, characters, locations, travel_system)
        game.current_location = "test_location"
        
        # Mock user inputs for the exploration cycle:
        # 1. Choose option 1 (Explore)
        # 2. Select character 1
        # 3. Select stat 1 (Strength)
        # 4. Choose option 4 (Quit)
        mock_input.side_effect = ["1", "1", "1", "4"]
        
        # Run the game for one cycle
        with patch.object(game, 'check_game_over', return_value=False):
            game.location_menu()
            self.assertFalse(game.continue_playing)  # Should be set to False by the quit option
        
        # Verify the expected outputs were printed
        mock_print.assert_any_call("A challenge appears!")
        mock_print.assert_any_call("Choose a party member:")
        mock_print.assert_any_call("Choose a stat for Test Character:")

if __name__ == '__main__':
    unittest.main()
