import json
import sys
import random
import os
from typing import List, Optional, Dict
from enum import Enum
from .model import EventStatus, Statistic, Character, Event
from .travel_system import TravelSystem, TravelEvent


class Location:
    def __init__(self, name: str, display_name: str, events: List[Event]):
        self.name = name
        self.display_name = display_name
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)



class Game:
    def __init__(self, parser, characters: List[Character], locations: Dict[str, Location], travel_system: TravelSystem):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.travel_system = travel_system
        self.current_location = None
        self.continue_playing = True

    def start(self):
        # Let the player choose a starting location
        print("Choose a starting location:")
        location_names = list(self.locations.keys())
        for idx, loc_name in enumerate(location_names):
            print(f"{idx + 1}. {self.locations[loc_name].display_name}")
        
        choice = int(self.parser.parse("Enter the number of your starting location: ")) - 1
        self.current_location = location_names[choice]
        
        print(f"\nYou begin your adventure in {self.locations[self.current_location].display_name}.\n")
        
        while self.continue_playing:
            self.location_menu()
            if self.check_game_over():
                self.continue_playing = False
        
        print("Game Over.")

    def location_menu(self):
        """Display menu of actions at the current location."""
        location = self.locations[self.current_location]
        
        print(f"\nYou are in {location.display_name}. What would you like to do?")
        print("1. Explore this location")
        print("2. Travel to another location")
        print("3. View party status")
        print("4. Quit game")
        
        choice = int(self.parser.parse("Enter your choice: "))
        
        if choice == 1:
            self.explore_location()
        elif choice == 2:
            self.travel_menu()
        elif choice == 3:
            self.show_party_status()
        elif choice == 4:
            self.continue_playing = False
        else:
            print("Invalid choice, please try again.")
    
    def explore_location(self):
        """Trigger a random event at the current location."""
        location = self.locations[self.current_location]
        event = location.get_event()
        event.execute(self.party, self.parser)
    
    def travel_menu(self):
        """Display menu of available travel destinations."""
        available_destinations = self.travel_system.get_available_destinations(self.current_location)
        
        if not available_destinations:
            print(f"There are no known routes from {self.locations[self.current_location].display_name}.")
            return
        
        print(f"\nFrom {self.locations[self.current_location].display_name}, you can travel to:")
        
        for idx, dest in enumerate(available_destinations):
            if dest in self.locations:
                print(f"{idx + 1}. {self.locations[dest].display_name}")
            else:
                print(f"{idx + 1}. {dest} (Unknown region)")
        
        print(f"{len(available_destinations) + 1}. Cancel travel")
        
        choice = int(self.parser.parse("Enter your choice: ")) - 1
        
        if choice >= 0 and choice < len(available_destinations):
            destination = available_destinations[choice]
            success = self.travel_system.execute_travel(
                self.current_location, destination, self.party, self.parser
            )
            
            if success:
                self.current_location = destination
                print(f"\nYou have arrived at {self.locations[self.current_location].display_name}.\n")
            else:
                print("\nYour journey was unsuccessful. You remain at your current location.\n")
    
    def show_party_status(self):
        """Display status of all party members."""
        print("\nParty Status:")
        for character in self.party:
            print(f"\n{character.name}")
            for stat in character.get_stats():
                print(f"  {stat.name}: {stat.value}")
    
    def check_game_over(self):
        """Check if the game should end."""
        return len(self.party) == 0


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def load_locations(locations_directory: str) -> Dict[str, Location]:
    """Load all locations and their events from JSON files."""
    locations = {}
    location_display_names = {
        "winterfell": "Winterfell",
        "kings_landing": "King's Landing",
        "the_wall": "The Wall",
        "dragonstone": "Dragonstone",
        "beyond_the_wall": "Beyond the Wall",
        "braavos": "Braavos",
        "the_eyrie": "The Eyrie",
        "the_iron_islands": "The Iron Islands",
        "dorne": "Dorne"
    }
    
    # First check if the directory exists
    if not os.path.exists(locations_directory):
        print(f"Warning: Location directory {locations_directory} not found.")
        # Create a default location as fallback
        locations["forest"] = Location("forest", "The Forest", [
            Event({
                "primary_attribute": "Intelligence",
                "secondary_attribute": "Strength",
                "prompt_text": "You discover an ancient puzzle in the forest. How do you approach it?",
                "pass": {"message": "Your intelligence allows you to solve the puzzle."},
                "fail": {"message": "You fail to solve the puzzle."},
                "partial_pass": {"message": "Your strength helps but doesn't fully solve the puzzle."}
            })
        ])
        return locations
    
    for filename in os.listdir(locations_directory):
        if filename.endswith('.json'):
            location_name = filename.split('.')[0]  # Remove .json extension
            
            if location_name not in location_display_names:
                display_name = location_name.replace('_', ' ').title()
            else:
                display_name = location_display_names[location_name]
            
            file_path = os.path.join(locations_directory, filename)
            events = load_events_from_json(file_path)
            
            if events:
                locations[location_name] = Location(location_name, display_name, events)
    
    return locations


def start_game():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    parser = UserInputParser()
    
    # Create party members
    characters = [
        Character("Arya"),
        Character("Jon"),
        Character("Tyrion")
    ]
    
    # Customize characters with different stat distributions
    characters[0].strength.value = 60
    characters[0].stealth.value = 80
    characters[0].intelligence.value = 65
    
    characters[1].strength.value = 75
    characters[1].endurance.value = 70
    characters[1].charisma.value = 60
    
    characters[2].intelligence.value = 85
    characters[2].cunning.value = 80
    characters[2].charisma.value = 75
    
    # Load locations
    locations_directory = os.path.join(project_dir, 'location_events')
    locations = load_locations(locations_directory)
    
    # Set up travel system
    travel_events_directory = os.path.join(project_dir, 'travel_events')
    travel_system = TravelSystem(travel_events_directory)
    
    # Create and start the game
    game = Game(parser, characters, locations, travel_system)
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    start_game()
