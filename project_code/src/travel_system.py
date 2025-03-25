adventure_game/src/travel_system.py
import os
import json
import random
from typing import List, Dict, Optional

from .model import Event, Character, EventStatus, Statistic

class TravelEvent(Event):
    """Event that occurs when traveling between locations."""
    
    def __init__(self, data: dict):
        super().__init__(data)
        self.from_location = data['from_location']
        self.to_location = data['to_location']

class TravelSystem:
    """System for handling travel between different locations in the game."""
    
    def __init__(self, travel_events_directory: str):
        self.travel_events = self._load_travel_events(travel_events_directory)
        
    def _load_travel_events(self, directory: str) -> Dict[str, Dict[str, List[TravelEvent]]]:
        """Load all travel events from JSON files in the specified directory."""
        events_by_route = {}
        
        if not os.path.exists(directory):
            print(f"Warning: Travel events directory {directory} not found.")
            return events_by_route
            
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    events_data = json.load(file)
                    
                    for event_data in events_data:
                        from_loc = event_data['from_location']
                        to_loc = event_data['to_location']
                        
                        if from_loc not in events_by_route:
                            events_by_route[from_loc] = {}
                        
                        if to_loc not in events_by_route[from_loc]:
                            events_by_route[from_loc][to_loc] = []
                            
                        events_by_route[from_loc][to_loc].append(TravelEvent(event_data))
        
        return events_by_route
    
    def get_travel_event(self, from_location: str, to_location: str) -> Optional[TravelEvent]:
        """Get a random travel event for the given route."""
        if from_location in self.travel_events and to_location in self.travel_events[from_location]:
            return random.choice(self.travel_events[from_location][to_location])
        return None
    
    def get_available_destinations(self, from_location: str) -> List[str]:
        """Get all possible destinations from the current location."""
        if from_location in self.travel_events:
            return list(self.travel_events[from_location].keys())
        return []
        
    def execute_travel(self, from_location: str, to_location: str, party: List[Character], parser) -> bool:
        """Execute a travel event between locations and return success status."""
        travel_event = self.get_travel_event(from_location, to_location)
        
        if not travel_event:
            print(f"No known route from {from_location} to {to_location}.")
            return False
            
        print(f"\nTraveling from {from_location} to {to_location}...\n")
        print(travel_event.prompt_text)
        
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        travel_event.resolve_choice(character, chosen_stat)
        
        # Return True if the travel was successful (PASS or PARTIAL_PASS)
        return travel_event.status != EventStatus.FAIL
