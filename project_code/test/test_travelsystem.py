import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import TravelSystem, TravelEvent, Character, EventStatus

class TestTravelSystem(unittest.TestCase):
    """Test the TravelSystem class and related functionality."""
    
    def setUp(self):
        """Set up test data before each test."""
        # Create mock travel events data
        self.travel_events_data = [
            {
                "from_location": "winterfell",
                "to_location": "kings_landing",
                "primary_attribute": "Endurance",
                "secondary_attribute": "Intelligence",
                "prompt_text": "The Kingsroad is long and dangerous. How will you handle the journey?",
                "pass": {"message": "You navigate the journey efficiently, arriving in good time."},
                "fail": {"message": "The journey is harder than expected, and you arrive exhausted."},
                "partial_pass": {"message": "You navigate the journey with some difficulties but arrive safely."}
            },
            {
                "from_location": "winterfell",
                "to_location": "the_wall",
                "primary_attribute": "Strength",
                "secondary_attribute": "Endurance",
                "prompt_text": "The harsh northern weather makes the journey difficult. How will you proceed?",
                "pass": {"message": "Your strength sees you through the harsh conditions."},
                "fail": {"message": "The cold and snow overwhelm your party, forcing a return to Winterfell."},
                "partial_pass": {"message": "You endure the journey, though it takes longer than planned."}
            }
        ]
        
        # Create a mock directory structure
        self.directory_structure = {
            'winterfell_to_kings_landing.json': self.travel_events_data[0:1],
            'winterfell_to_the_wall.json': self.travel_events_data[1:2]
        }
        
        # Create test characters
        self.test_character = Character("Jon Snow")
        self.test_character.endurance.value = 80
        self.test_character.intelligence.value = 70
        self.test_character.strength.value = 85
        
        self.party = [self.test_character]
        
        # Create mock parser
        self.mock_parser = MagicMock()
        self.mock_parser.select_party_member.return_value = self.test_character
        self.mock_parser.select_stat.return_value = self.test_character.endurance
    
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def create_travel_system(self, mock_json_load, mock_file_open, mock_listdir):
        """Helper method to create a travel system with mocked file operations."""
        mock_listdir.return_value = list(self.directory_structure.keys())
        
        # Set up json.load to return the appropriate data for each file
        mock_json_load.side_effect = list(self.directory_structure.values())
        
        # Create and return the travel system
        return TravelSystem('/fake/path')
    
    def test_travel_event_initialization(self):
        """Test initialization of a TravelEvent."""
        event = TravelEvent(self.travel_events_data[0])
        
        self.assertEqual(event.from_location, "winterfell")
        self.assertEqual(event.to_location, "kings_landing")
        self.assertEqual(event.primary_attribute, "Endurance")
        self.assertEqual(event.secondary_attribute, "Intelligence")
        self.assertEqual(event.prompt_text, self.travel_events_data[0]["prompt_text"])
    
    def test_get_travel_event(self):
        """Test getting a travel event for a specific route."""
        travel_system = self.create_travel_system()
        
        # Get event for existing route
        event = travel_system.get_travel_event("winterfell", "kings_landing")
        
        self.assertIsNotNone(event)
        self.assertIsInstance(event, TravelEvent)
        self.assertEqual(event.from_location, "winterfell")
        self.assertEqual(event.to_location, "kings_landing")
        
        # Test non-existent route
        event = travel_system.get_travel_event("kings_landing", "winterfell")
        self.assertIsNone(event)
    
    def test_get_available_destinations(self):
        """Test getting available destinations from a location."""
        travel_system = self.create_travel_system()
        
        # Get destinations from winterfell
        destinations = travel_system.get_available_destinations("winterfell")
        
        self.assertEqual(len(destinations), 2)
        self.assertIn("kings_landing", destinations)
        self.assertIn("the_wall", destinations)
        
        # Test non-existent location
        destinations = travel_system.get_available_destinations("braavos")
        self.assertEqual(destinations, [])
    
    @patch('builtins.print')
    def test_execute_travel_success(self, mock_print):
        """Test executing a successful travel event."""
        travel_system = self.create_travel_system()
        
        # Set up mock parser to return endurance (primary attribute)
        self.mock_parser.select_stat.return_value = self.test_character.endurance
        
        # Execute travel
        result = travel_system.execute_travel(
            "winterfell", "kings_landing", self.party, self.mock_parser
        )
        
        # Check result is successful
        self.assertTrue(result)
        
        # Verify method calls
        self.mock_parser.select_party_member.assert_called_once_with(self.party)
        self.mock_parser.select_stat.assert_called_once_with(self.test_character)
    
    @patch('builtins.print')
    def test_execute_travel_failure(self, mock_print):
        """Test executing a failed travel event."""
        travel_system = self.create_travel_system()
        
        # Create a TravelEvent that will return FAIL
        mock_event = MagicMock()
        mock_event.prompt_text = "Test prompt"
        mock_event.status = EventStatus.FAIL
        
        # Replace get_travel_event to return our mock event
        travel_system.get_travel_event = MagicMock(return_value=mock_event)
        
        # Execute travel
        result = travel_system.execute_travel(
            "winterfell", "kings_landing", self.party, self.mock_parser
        )
        
        # Check result is failure
        self.assertFalse(result)
    
    @patch('builtins.print')
    def test_execute_travel_no_route(self, mock_print):
        """Test executing travel with no route available."""
        travel_system = self.create_travel_system()
        
        # Execute travel with non-existent route
        result = travel_system.execute_travel(
            "braavos", "pentos", self.party, self.mock_parser
        )
        
        # Check result is failure
        self.assertFalse(result)
        
        # Check appropriate message was printed
        mock_print.assert_any_call("No known route from braavos to pentos.")

if __name__ == '__main__':
    unittest.main()
