import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Game, Character, Location, Event, TravelSystem

class TestGame(unittest.TestCase):
    """Test the Game class and its methods."""
    
    def setUp(self):
        """Set up test data before each test."""
        # Create mock parser
        self.mock_parser = MagicMock()
        
        # Create test characters
        self.characters = [
            Character("Arya"),
            Character("Jon"),
            Character("Tyrion")
        ]
        
        # Create test events
        self.winterfell_events = [
            Event({
                "primary_attribute": "Intelligence",
                "secondary_attribute": "Stealth",
                "prompt_text": "The Godswood holds secrets. How will you uncover them?",
                "pass": {"message": "You discover hidden scrolls beneath the Heart Tree."},
                "fail": {"message": "Your search reveals nothing of value."},
                "partial_pass": {"message": "You find some clues but need more information."}
            })
        ]
        
        self.kings_landing_events = [
            Event({
                "primary_attribute": "Charisma",
                "secondary_attribute": "Cunning",
                "prompt_text": "Court intrigues surround you. How do you navigate them?",
                "pass": {"message": "You charm the courtiers and learn valuable secrets."},
                "fail": {"message": "You become entangled in court politics and gain enemies."},
                "partial_pass": {"message": "You maintain your position without gaining much influence."}
            })
        ]
        
        # Create test locations
        self.locations = {
            "winterfell": Location("winterfell", "Winterfell", self.winterfell_events),
            "kings_landing": Location("kings_landing", "King's Landing", self.kings_landing_events)
        }
        
        # Create mock travel system
        self.mock_travel_system = MagicMock(spec=TravelSystem)
        self.mock_travel_system.get_available_destinations.return_value = ["kings_landing"]
        self.mock_travel_system.execute_travel.return_value = True
        
        # Create game instance
        self.game = Game(
            self.mock_parser,
            self.characters,
            self.locations,
            self.mock_travel_system
        )
        
        # Set initial location
        self.game.current_location = "winterfell"
    
    def test_game_initialization(self):
        """Test that a game is correctly initialized."""
        self.assertEqual(self.game.parser, self.mock_parser)
        self.assertEqual(self.game.party, self.characters)
        self.assertEqual(self.game.locations, self.locations)
        self.assertEqual(self.game.travel_system, self.mock_travel_system)
        self.assertEqual(self.game.current_location, "winterfell")
        self.assertTrue(self.game.continue_playing)
    
    @patch('builtins.print')
    def test_show_party_status(self, mock_print):
        """Test displaying party status."""
        self.game.show_party_status()
        
        # Check that character names were printed
        mock_print.assert_any_call("\nParty Status:")
        mock_print.assert_any_call("\nArya")
        mock_print.assert_any_call("\nJon")
        mock_print.assert_any_call("\nTyrion")
    
    def test_check_game_over_with_party(self):
        """Test game over check with party members remaining."""
        self.assertFalse(self.game.check_game_over())
    
    def test_check_game_over_no_party(self):
        """Test game over check with no party members."""
        self.game.party = []
        self.assertTrue(self.game.check_game_over())
    
    @patch('builtins.print')
    def test_explore_location(self, mock_print):
        """Test exploring a location."""
        # Get a reference to the event for verification
        location = self.locations["winterfell"]
        event = location.events[0]
        
        # Execute exploration
        self.game.explore_location()
        
        # Check that the event was executed
        mock_print.assert_any_call(event.prompt_text)
    
    @patch('builtins.print')
    def test_travel_menu_with_destinations(self, mock_print):
        """Test travel menu with available destinations."""
        # Mock parser to return valid choice
        self.mock_parser.parse.return_value = "1"  # Select first destination
        
        # Call travel menu
        self.game.travel_menu()
        
        # Check that destinations were displayed
        mock_print.assert_any_call("\nFrom Winterfell, you can travel to:")
        mock_print.assert_any_call("1. King's Landing")
        
        # Check that travel was executed
        self.mock_travel_system.execute_travel.assert_called_once_with(
            "winterfell", "kings_landing", self.game.party, self.mock_parser
        )
        
        # Check that current location was updated
        self.assertEqual(self.game.current_location, "kings_landing")
    
    @patch('builtins.print')
    def test_travel_menu_no_destinations(self, mock_print):
        """Test travel menu with no available destinations."""
        # Mock no available destinations
        self.mock_travel_system.get_available_destinations.return_value = []
        
        # Call travel menu
        self.game.travel_menu()
        
        # Check appropriate message was displayed
        mock_print.assert_called_with("There are no known routes from Winterfell.")
    
    @patch('builtins.print')
    def test_location_menu(self, mock_print):
        """Test location menu options."""
        # Test each menu option
        
        # 1. Explore location
        self.mock_parser.parse.return_value
