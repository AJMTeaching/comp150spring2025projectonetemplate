import json
import sys
import random
from typing import List, Optional
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
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Intelligence is a measure of cognitive ability.")
        # Add more stats as needed

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence]  # Extend this list if there are more stats


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





class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)




class GameState:
    def __init__(self):
        self.visited_locations = set()  # Tracks unique locations visited
        self.successful_events = 0      # Counts successful events
        self.party = []                 # Reference to the party members




class Game:
     def __init__(self, parser, characters: List[Character], locations: Dict[str, Location], travel_system: TravelSystem):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.travel_system = travel_system
        self.current_location = None
        self.continue_playing = True
        
        # Initialize game state tracking
        self.game_state = GameState()
        self.game_state.party = self.party

    def start(self):
    while self.continue_playing:
        # Randomly select a location and trigger an event
        location = random.choice(self.locations)
        event = location.get_event()
        event.execute(self.party, self.parser)        
        
        # Track visited locations
        if self.current_location:
            self.game_state.visited_locations.add(self.current_location)
        
        # Check for victory condition
        victory = check_win_condition(self.game_state)
        if victory:
            self.display_victory()
            self.continue_playing = False
            break
        
        # Check for game over condition
        if self.check_game_over():
            self.continue_playing = False

    print("Game Over.")



    def check_game_over(self):
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


def start_game():
    parser = UserInputParser()
    characters = [Character(f"Character_{i}") for i in range(3)]

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()

map_object = map(function, iterable)

#!/usr/bin/env python3
"""
Setup script for Game of Thrones Adventure game.
This script will:
1. Create all location JSON files
2. Set up the game map module
3. Update the main game code
"""

import os
import json
import shutil
import sys

# Define the root directory
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(ROOT_DIR, 'project_code')

# Game of Thrones locations data
got_locations = {
    "winterfell": [
        {
            "primary_attribute": "Intelligence",
            "secondary_attribute": "Stealth",
            "prompt_text": "The Godswood of Winterfell holds many secrets. You've heard whispers of hidden Stark treasures beneath the Heart Tree. How will you discover them?",
            "pass": {
                "message": "Through your knowledge of Old Northern legends and careful observation, you uncover a small opening beneath the Heart Tree, revealing a cache of Valyrian steel daggers and ancient scrolls."
            },
            "fail": {
                "message": "Your clumsy search alerts the guards. They escort you from the Godswood, warning never to disturb the sacred place again."
            },
            "partial_pass": {
                "message": "You find markings that suggest something is hidden, but can't quite determine how to access it. Perhaps someone with knowledge of Stark history could help."
            }
        },
        {
            "primary_attribute": "Strength",
            "secondary_attribute": "Endurance",
            "prompt_text": "Winter has come to Winterfell. The battlements need clearing of dangerous ice before they collapse. The task requires working in the biting cold for hours.",
            "pass": {
                "message": "You clear the ice systematically, saving the battlements from collapse and earning the respect of the Stark household guards."
            },
            "fail": {
                "message": "The cold proves too much, and your hands grow numb. You retreat inside before completing the task, leaving the battlements vulnerable."
            },
            "partial_pass": {
                "message": "You clear the most dangerous sections before the cold forces you to stop. The battlements are safer, but not completely secure."
            }
        },
        {
            "primary_attribute": "Charisma",
            "secondary_attribute": "Intelligence",
            "prompt_text": "Lord Stark is holding court to settle a dispute between two Northern houses. You have information that could help, but speaking out of turn is frowned upon.",
            "pass": {
                "message": "You respectfully request permission to speak and present your information clearly. Lord Stark thanks you for your contribution, which helps settle the dispute justly."
            },
            "fail": {
                "message": "Your interruption is seen as disrespectful. Lord Stark has you removed from the hall, and your information goes unheard."
            },
            "partial_pass": {
                "message": "You manage to convey your information, but your delivery lacks tact. The information helps, but Lord Stark reminds you to mind courtly protocols in the future."
            }
        }
    ],
    "kings_landing": [
        {
            "primary_attribute": "Cunning",
            "secondary_attribute": "Charisma",
            "prompt_text": "A feast is being held in the Red Keep. You overhear whispers of a plot against the crown. How do you handle this sensitive information?",
            "pass": {
                "message": "Through subtle conversation and careful maneuvering, you identify the conspirators and discreetly inform the appropriate authorities without revealing your source."
            },
            "fail": {
                "message": "Your clumsy inquiries alert the conspirators. They spread false rumors about you, and you find yourself unwelcome at court."
            },
            "partial_pass": {
                "message": "You learn some details of the plot but not enough to identify the conspirators. The information you provide helps increase security, but the threat remains."
            }
        },
        {
            "primary_attribute": "Stealth",
            "secondary_attribute": "Intelligence",
            "prompt_text": "Important documents are kept in the Tower of the Hand. You need to view them without permission to uncover the truth about a matter of grave importance.",
            "pass": {
                "message": "You successfully slip past the guards, locate the documents, memorize their contents, and leave without detection, gaining crucial information."
            },
            "fail": {
                "message": "You're caught by the guards and thrown into the Black Cells, accused of espionage against the crown."
            },
            "partial_pass": {
                "message": "You reach the documents but only have time to glimpse them before nearly being discovered. You escape, but with incomplete information."
            }
        },
        {
            "primary_attribute": "Charisma",
            "secondary_attribute": "Cunning",
            "prompt_text": "You need to gain access to a closed Small Council meeting. The guards at the door are strictly following orders about who may enter.",
            "pass": {
                "message": "With a combination of confidence, persuasive half-truths, and knowledge of courtly protocols, you convince the guards you have legitimate business inside."
            },
            "fail": {
                "message": "The guards see through your deception and threaten to report you to the City Watch for attempting to interfere with royal business."
            },
            "partial_pass": {
                "message": "You cannot get inside, but you convince one of the guards to deliver a message to someone within, partially achieving your goal."
            }
        }
    ],
    # ... more locations would follow but truncated for brevity
}


def create_game_map_module():
    """Create the game_map.py module in the src directory."""
    game_map_content = """
# project_code/src/game_map.py

class GameMap:
    \"\"\"A map system for the Game of Thrones adventure game.\"\"\"
    
    def __init__(self):
        self.locations = [
            "winterfell", "kings_landing", "the_wall", "dragonstone", 
            "beyond_the_wall", "braavos", "the_eyrie", "the_iron_islands", "dorne"
        ]
        self.location_display_names = {
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
        self.current_location = None
        self.map_ascii = \"\"\"
                                      The North
                                     /        \\\\
                                    /          \\\\
               The Wall -----------+            \\\\
               /                   |             \\\\
              /                    |              \\\\
     Beyond the Wall              /                \\\\
                                 /                  \\\\
                                /                    \\\\
                        Winterfell                    \\\\
                             |                         \\\\
                             |                          \\\\
                         The Twins                       |
                             |                           |
                             |        The Eyrie          |
                             |            |              |
                       Riverrun----------+               |
                             |                           |
      The Iron Islands-------+                           |
                             |                           |
                             |                          /
                       Casterly Rock                   /
                             |                        /
                        King's Landing---------------+
                            / \\\\                     /
                           /   \\\\                   /
                          /     \\\\                 /
                    Dragonstone  \\\\               /
                                  Highgarden    /
                                        \\\\      /
                                         \\\\    /
                                         Dorne
        \"\"\"
        
    def show_map(self):
        \"\"\"Display the ASCII map with current location marked if set.\"\"\"
        if self.current_location:
            display_name = self.location_display_names[self.current_location]
            # Create a highlighted version with stars for the current location
            highlighted_loc = f"***{display_name}***"
            # Simple highlighting - in a real game you could use colors
            map_with_location = self.map_ascii.replace(display_name, highlighted_loc)
            return map_with_location
        else:
            return self.map_ascii
            
    def set_location(self, location):
        \"\"\"Set the current team location.\"\"\"
        if location in self.locations:
            self.current_location = location
            return True
        else:
            return False
            
    def get_available_locations(self):
        \"\"\"Return list of all game locations with display names.\"\"\"
        return [self.location_display_names[loc] for loc in self.locations]
        
    def get_current_location(self):
        \"\"\"Return the current location name.\"\"\"
        if self.current_location:
            return self.location_display_names[self.current_location]
        return None
"""
    
    game_map_path = os.path.join(PROJECT_DIR, 'src', 'game_map.py')
    with open(game_map_path, 'w') as f:
        f.write(game_map_content.strip())
    print(f"Created {game_map_path}")


def create_location_json_files():
    """Create JSON files for each Game of Thrones location."""
    location_events_dir = os.path.join(PROJECT_DIR, 'location_events')
    for location_name, events in got_locations.items():
        file_path = os.path.join(location_events_dir, f"{location_name}.json")
        with open(file_path, 'w') as f:
            json.dump(events, f, indent=2)
        print(f"Created {file_path}")


def update_main_game_file():
    """Update the main.py file with Game of Thrones specific code and integrate travel system."""
    main_path = os.path.join(PROJECT_DIR, 'src', 'main.py')
    
    # Get the travel system integration code
    from src.travel_system import integrate_travel_system
    main_game_updates = integrate_travel_system()
    
    # Write the updated main.py
    with open(main_path, 'w') as f:
        f.write(main_game_updates)
    
    print(f"Updated {main_path} with travel system integration")


def setup():
    """Set up the Game of Thrones adventure game."""
    print("Setting up Game of Thrones Adventure Game...")
    
    # Create location JSON files
    create_location_json_files()
    
    # Create game map module
    create_game_map_module()
    
    # Create travel system module
    create_travel_system_module()
    
    # Create travel events directory
    travel_events_dir = os.path.join(PROJECT_DIR, 'travel_events')
    os.makedirs(travel_events_dir, exist_ok=True)
    
    # Update main game file
    update_main_game_file()
    
    print("\nSetup complete! To run the game, execute:")
    print("python project_code/src/main.py")


if __name__ == "__main__":
    setup()

