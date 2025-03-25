import json
import sys
import random
import os
from typing import List, Optional, Dict
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.strength = Statistic("Strength", value=50, description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", value=50, description="Intelligence is a measure of cognitive ability.")
        self.charisma = Statistic("Charisma", value=50, description="Charisma is a measure of social influence.")
        self.stealth = Statistic("Stealth", value=50, description="Stealth is a measure of ability to remain unseen.")
        self.cunning = Statistic("Cunning", value=50, description="Cunning is a measure of cleverness and deception.")
        self.endurance = Statistic("Endurance", value=50, description="Endurance is a measure of stamina and resilience.")

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence, self.charisma, self.stealth, self.cunning, self.endurance]


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


class TravelEvent(Event):
    def __init__(self, data: dict):
        super().__init__(data)
        self.from_location = data['from_location']
        self.to_location = data['to_location']


class Location:
    def __init__(self, name: str, display_name: str, events: List[Event]):
        self.name = name
        self.display_name = display_name
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)


class TravelSystem:
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

def show_map(self):
    """Display the ASCII map of Westeros."""
    from project_code.src.game_map import GameMap
    game_map = GameMap()
    game_map.set_location(self.current_location)
    print(game_map.show_map())

if __name__ == '__main__':
    start_game()
