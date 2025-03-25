import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Location, Event

class TestLocation(unittest.TestCase):
    """Test the Location class and its methods."""
    
    def setUp(self):
        """Set up test data before each test."""
        # Create test events
        self.test_events = [
            MagicMock(spec=Event),
            MagicMock(spec=Event),
            MagicMock(spec=Event)
        ]
        
        # Create a location
        self.location = Location("winterfell", "Winterfell", self.test_events)
    
    def test_location_initialization(self):
        """Test that a location is correctly initialized."""
        self.assertEqual(self.location.name, "winterfell")
        self.assertEqual(self.location.display_name, "Winterfell")
        self.assertEqual(self.location.events, self.test_events)
    
    @patch('random.choice')
    def test_get_event(self, mock_choice):
        """Test getting a random event from the location."""
        # Set up the mock to return a specific event
        expected_event = self.test_events[1]
        mock_choice.return_value = expected_event
        
        # Get an event
        event = self.location.get_event()
        
        # Verify random.choice was called with the events list
        mock_choice.assert_called_once_with(self.test_events)
        
        # Verify the correct event was returned
        self.assertEqual(event, expected_event)
    
    def test_get_event_with_empty_events(self):
        """Test getting an event when the location has no events."""
        # Create a location with no events
        empty_location = Location("empty", "Empty Location", [])
        
        # This should raise an IndexError when random.choice is called on an empty list
        with self.assertRaises(IndexError):
            empty_location.get_event()

if __name__ == '__main__':
    unittest.main()
