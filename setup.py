from setuptools import setup, find_packages

setup(
    name="adventure-game",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'adventure-game=adventure_game.src.main:start_game',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A text-based adventure game with Game of Thrones themes",
    keywords="game, adventure, text-based, game-of-thrones",
    url="https://github.com/yourusername/adventure-game",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
)
#!/usr/bin/env python3
"""
Setup script for Game of Thrones Adventure game.
This script will:
1. Create the proper directory structure
2. Fix location event files
3. Ensure travel events are properly formatted
4. Fix main game code files
"""

import os
import json
import shutil
import sys

# Define the root directory (where this script is)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(ROOT_DIR, 'project_code')

def create_directory_structure():
    """Create the proper directory structure for the game."""
    print("Creating directory structure...")
    
    # Ensure the main directories exist
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'location_events'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'travel_events'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'test'), exist_ok=True)

def write_main_py():
    """Write the fixed main.py file."""
    print("Writing main.py...")
    
    main_py_path = os.path.join(PROJECT_DIR, 'src', 'main.py')
    with open(main_py_path, 'w') as f:
        f.write(MAIN_PY_CONTENT)

def write_game_map_py():
    """Write the game_map.py file."""
    print("Writing game_map.py...")
    
    game_map_path = os.path.join(PROJECT_DIR, 'src', 'game_map.py')
    with open(game_map_path, 'w') as f:
        f.write(GAME_MAP_PY_CONTENT)

def write_location_event_files():
    """Write the location event JSON files."""
    print("Writing location event files...")
    
    location_events_dir = os.path.join(PROJECT_DIR, 'location_events')
    
    # Write each location event file
    location_files = {
        'winterfell.json': WINTERFELL_EVENTS,
        'kings_landing.json': KINGS_LANDING_EVENTS,
        'the_wall.json': THE_WALL_EVENTS,
        'beyond_the_wall.json': BEYOND_THE_WALL_EVENTS,
        'dragonstone.json': DRAGONSTONE_EVENTS,
        'braavos.json': BRAAVOS_EVENTS,
        'the_eyrie.json': THE_EYRIE_EVENTS,
        'the_iron_islands.json': THE_IRON_ISLANDS_EVENTS,
        'dorne.json': DORNE_EVENTS
    }
    
    for filename, content in location_files.items():
        file_path = os.path.join(location_events_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
            print(f"  Created {file_path}")

def ensure_travel_events():
    """Make sure travel event files are properly formatted."""
    print("Checking travel event files...")
    
    travel_events_dir = os.path.join(PROJECT_DIR, 'travel_events')
    
    # The existing travel event files seem properly formatted already
    # We'll just make sure they have .json extensions
    for filename in os.listdir(travel_events_dir):
        if not filename.endswith('.json'):
            original_path = os.path.join(travel_events_dir, filename)
            new_path = os.path.join(travel_events_dir, f"{filename}.json")
            shutil.move(original_path, new_path)
            print(f"  Renamed {filename} to {filename}.json")

# Content for location event files
WINTERFELL_EVENTS = """[
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
]"""

KINGS_LANDING_EVENTS = """[
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
]"""

THE_WALL_EVENTS = """[
  {
    "primary_attribute": "Endurance",
    "secondary_attribute": "Strength",
    "prompt_text": "A ferocious blizzard has hit Castle Black. The Night's Watch must patrol the top of the Wall despite the dangerous conditions to watch for wildling activity.",
    "pass": {
      "message": "You complete your patrol despite the brutal cold, spotting a small wildling scouting party and alerting the Watch in time to prepare."
    },
    "fail": {
      "message": "The cold overwhelms you, and you're forced to return early, missing the approach of wildling scouts who gather valuable intelligence on Castle Black's defenses."
    },
    "partial_pass": {
      "message": "You endure most of your patrol but must cut it short. You spot signs of wildling activity but cannot determine their numbers or exact location."
    }
  },
  {
    "primary_attribute": "Intelligence",
    "secondary_attribute": "Cunning",
    "prompt_text": "The Lord Commander has received a cryptic message from Eastwatch-by-the-Sea. It seems to be in code, and understanding it quickly could be vital.",
    "pass": {
      "message": "You decipher the code, revealing that a fleet of wildling ships has been spotted heading for Eastwatch. The Watch has time to send reinforcements."
    },
    "fail": {
      "message": "The message remains a mystery to you. Days later, news arrives that Eastwatch was attacked, and the Watch was unprepared."
    },
    "partial_pass": {
      "message": "You understand parts of the message, enough to know there's danger at Eastwatch, but not the nature or timing of the threat."
    }
  },
  {
    "primary_attribute": "Strength", 
    "secondary_attribute": "Endurance",
    "prompt_text": "The winch elevator to the top of the Wall has broken. Urgent supplies need to be carried up the steps to the sentries above before they freeze.",
    "pass": {
      "message": "You carry the heavy supplies all the way up the hundreds of ice-carved steps, ensuring the sentries can maintain their vital watch."
    },
    "fail": {
      "message": "The burden proves too much. You cannot make it more than halfway up. Some sentries are forced to abandon their posts due to lack of supplies."
    },
    "partial_pass": {
      "message": "You manage to carry the most essential supplies to the top, though you have to leave some behind. The sentries can continue their watch but with limited resources."
    }
  }
]"""

BEYOND_THE_WALL_EVENTS = """[
  {
    "primary_attribute": "Endurance",
    "secondary_attribute": "Intelligence",
    "prompt_text": "Your party is caught in a deadly blizzard beyond the Wall. You need to find shelter quickly before freezing to death in the hostile wilderness.",
    "pass": {
      "message": "You lead your party through the blinding snow, using your knowledge of winter survival to find a hidden cave. Everyone survives the night as the blizzard rages outside."
    },
    "fail": {
      "message": "The cold overwhelms your party. By morning, two companions have severe frostbite, and everyone's supplies are dangerously depleted."
    },
    "partial_pass": {
      "message": "You find minimal shelter behind a rock formation. It's enough to survive the night, but everyone suffers from the cold, weakening the party for days to come."
    }
  },
  {
    "primary_attribute": "Stealth",
    "secondary_attribute": "Cunning",
    "prompt_text": "Your scouting party has spotted a wildling camp ahead. You need to observe their numbers and intentions without being discovered.",
    "pass": {
      "message": "You move like a ghost through the snow, getting close enough to count their warriors and overhear their plans to raid a village south of the Wall."
    },
    "fail": {
      "message": "A wildling scout spots you. The alarm is raised, and your party must flee, gaining no information and revealing your presence in the area."
    },
    "partial_pass": {
      "message": "You observe the camp from a distance, gauging their approximate numbers but unable to learn their intentions without getting closer."
    }
  },
  {
    "primary_attribute": "Strength",
    "secondary_attribute": "Endurance",
    "prompt_text": "A massive snow-covered ravine blocks your path. The nearest bridge is days away, but a fallen tree might serve as a crossing if it can be moved into position.",
    "pass": {
      "message": "You organize and lead the effort to move the massive tree trunk. With tremendous effort, you create a stable bridge, saving days of dangerous travel."
    },
    "fail": {
      "message": "Despite your best efforts, the tree is too heavy to position properly. You must abandon the attempt and take the long route around, losing precious time."
    },
    "partial_pass": {
      "message": "You manage to position the tree, but it's not entirely stable. Everyone crosses safely, but slowly and carefully, saving some but not all of the time a proper bridge would have."
    }
  }
]"""

DRAGONSTONE_EVENTS = """[
  {
    "primary_attribute": "Intelligence",
    "secondary_attribute": "Cunning",
    "prompt_text": "The ancient libraries of Dragonstone contain tomes about Valyrian dragonlore. You seek information about controlling dragons in these forbidden texts.",
    "pass": {
      "message": "You find and translate a previously overlooked Valyrian scroll detailing the bonding process between dragon and rider, knowledge that could prove invaluable."
    },
    "fail": {
      "message": "The complex Valyrian texts confound you, and you waste days finding nothing of value. A suspicious maester reports your activities to the castle's lord."
    },
    "partial_pass": {
      "message": "You discover fragments of useful information about dragon behaviors, but nothing specific about controlling them. The knowledge is interesting but limited in practical use."
    }
  },
  {
    "primary_attribute": "Stealth",
    "secondary_attribute": "Intelligence",
    "prompt_text": "Rumor has it that there's a hidden chamber beneath Dragonstone containing dragon eggs. The entrance is said to be somewhere in the lower levels of the castle.",
    "pass": {
      "message": "Moving silently through the castle's underbelly, you discover a hidden passage behind an ancient Targaryen sigil. It leads to a small chamber with what appear to be petrified dragon eggs."
    },
    "fail": {
      "message": "Your searching attracts the attention of the castle guards. You're apprehended and questioned about your suspicious activities."
    },
    "partial_pass": {
      "message": "You find evidence of a sealed passage that might lead to the chamber, but cannot determine how to open it without tools and more time."
    }
  },
  {
    "primary_attribute": "Endurance",
    "secondary_attribute": "Strength",
    "prompt_text": "A powerful storm has damaged the docks of Dragonstone. Ships cannot land with crucial supplies unless repairs are made quickly in the harsh weather.",
    "pass": {
      "message": "You work tirelessly through the storm, directing the repair efforts and participating in the heavy labor. The dock is repaired in time for the supply ships to land."
    },
    "fail": {
      "message": "The combination of wind, rain, and exhaustion defeats you. The repairs remain incomplete, and the supply ships are forced to return to the mainland."
    },
    "partial_pass": {
      "message": "You manage to repair enough of the dock for small boats to land, but larger ships with the bulk of the supplies must wait for better conditions."
    }
  }
]"""

BRAAVOS_EVENTS = """[
  {
    "primary_attribute": "Stealth",
    "secondary_attribute": "Cunning",
    "prompt_text": "You need information from inside the House of Black and White, the temple of the Faceless Men. Few enter this place and leave unchanged—if they leave at all.",
    "pass": {
      "message": "You slip into the temple unnoticed during a ceremony, hiding in the shadows as the Faceless Men perform their rituals. You learn their secrets and escape before anyone notices your presence."
    },
    "fail": {
      "message": "A Faceless Man spots you immediately upon entry. You awaken outside the temple with no memory of what happened inside, your task utterly failed."
    },
    "partial_pass": {
      "message": "You observe the outer chambers of the temple but cannot penetrate deeper without risking detection. You gather some information about their customs but nothing truly valuable."
    }
  },
  {
    "primary_attribute": "Charisma",
    "secondary_attribute": "Intelligence",
    "prompt_text": "You need a loan from the Iron Bank of Braavos for your important mission. The bankers are notoriously strict and skeptical, especially with foreigners.",
    "pass": {
      "message": "Your eloquent presentation and compelling arguments convince the Iron Bank representatives of the value of your venture. They grant you the loan with reasonable terms."
    },
    "fail": {
      "message": "The bankers dismiss your request outright. Your reputation in Braavos is damaged, and no financial institution will deal with you."
    },
    "partial_pass": {
      "message": "The Iron Bank offers you a loan, but with such harsh terms and high interest that it may cause more problems than it solves."
    }
  },
  {
    "primary_attribute": "Cunning",
    "secondary_attribute": "Stealth",
    "prompt_text": "You must navigate the political intrigues of Braavos to secure an alliance with an influential merchant prince. Many seek his favor, and he is known for testing potential allies.",
    "pass": {
      "message": "You deftly maneuver through the complex web of Braavosi politics, identifying the merchant prince's true desires and leveraging them to secure his support."
    },
    "fail": {
      "message": "You misjudge the political landscape and offend the merchant prince. Not only do you fail to secure his alliance, but he actively works against your interests."
    },
    "partial_pass": {
      "message": "The merchant prince remains neutral toward you, neither hindering nor helping your cause. He offers a minor trade agreement as a gesture of respect for your efforts."
    }
  }
]"""

THE_EYRIE_EVENTS = """[
  {
    "primary_attribute": "Strength",
    "secondary_attribute": "Endurance",
    "prompt_text": "The High Road to the Eyrie is treacherous, especially with mountain clans attacking travelers. Your party must reach the Gates of the Moon safely.",
    "pass": {
      "message": "You lead your party skillfully through the mountains, fighting off a mountain clan ambush with impressive strength. You arrive at the Gates of the Moon without casualties."
    },
    "fail": {
      "message": "Your party is scattered by an ambush from the Stone Crows. By the time you regroup, you've lost valuable time and resources, and some members bear injuries."
    },
    "partial_pass": {
      "message": "You repel the mountain clan attack, but not without cost. Your party reaches the Gates of the Moon, though with minor injuries and depleted supplies."
    }
  },
  {
    "primary_attribute": "Intelligence",
    "secondary_attribute": "Charisma",
    "prompt_text": "Lady Arryn is known for her paranoia and overprotection of her son. You need her permission to continue your mission in the Vale.",
    "pass": {
      "message": "You carefully frame your request to appeal to Lady Arryn's concern for her son's future, convincing her that your mission serves House Arryn's interests."
    },
    "fail": {
      "message": "Lady Arryn becomes convinced you pose a threat to her son. She refuses your request and orders you to leave the Eyrie immediately."
    },
    "partial_pass": {
      "message": "Lady Arryn remains suspicious but allows you limited access to the Vale, under constant supervision by House Arryn guards."
    }
  },
  {
    "primary_attribute": "Stealth",
    "secondary_attribute": "Intelligence",
    "prompt_text": "You need to retrieve an important document from the Eyrie's maester without drawing attention. The maester is loyal to House Arryn and watches his archives carefully.",
    "pass": {
      "message": "Under cover of night, you slip into the maester's study, locate the document, make a copy, and return everything exactly as you found it, leaving no trace of your visit."
    },
    "fail": {
      "message": "The maester catches you in his study. Your excuses fall flat, and you're brought before Lady Arryn to answer for your suspicious behavior."
    },
    "partial_pass": {
      "message": "You find the document but only have time to read it quickly, not copy it fully, before you must leave to avoid detection. You gain partial knowledge of its contents."
    }
  }
]"""

THE_IRON_ISLANDS_EVENTS = """[
  {
    "primary_attribute": "Endurance",
    "secondary_attribute": "Strength",
    "prompt_text": "A fierce storm has hit the Iron Islands while you're at sea. Your ship is in danger of capsizing as massive waves crash over the deck.",
    "pass": {
      "message": "You work tirelessly at the rigging and sails, guiding the ship through the tempest with exceptional seamanship. Your ship reaches Pyke largely intact."
    },
    "fail": {
      "message": "The storm overwhelms you and your crew. Your ship is badly damaged and barely limps to shore. The Ironborn mock your poor seamanship."
    },
    "partial_pass": {
      "message": "You keep the ship afloat but lose much of your cargo to the sea. The Ironborn respect your survival but note that a true ironborn would have saved the cargo too."
    }
  },
  {
    "primary_attribute": "Cunning",
    "secondary_attribute": "Charisma",
    "prompt_text": "You must negotiate with the Ironborn captain for passage to the mainland. Ironborn respect strength and cunning, not gold.",
    "pass": {
      "message": "You challenge the captain to a game of wits, impressing him with your cunning. He agrees to take you to the mainland, considering it an interesting diversion."
    },
    "fail": {
      "message": "The captain finds your approach dishonorable and weak. He refuses your request and shares the tale of your failure with other captains, who also refuse you passage."
    },
    "partial_pass": {
      "message": "The captain agrees to take you part of the way, but insists you prove yourself by working as part of his crew during the journey."
    }
  },
  {
    "primary_attribute": "Strength",
    "secondary_attribute": "Endurance",
    "prompt_text": "A rivalry between Ironborn crews erupts into a brawl at the harbor. You're caught in the middle and must prove your worth or be seen as weak.",
    "pass": {
      "message": "You hold your own in the fight, demonstrating strength that earns the respect of the Ironborn. They begin to treat you as a worthy warrior."
    },
    "fail": {
      "message": "You're quickly overwhelmed in the brawl. The Ironborn laugh at your weakness, and your reputation suffers throughout the Iron Islands."
    },
    "partial_pass": {
      "message": "You avoid the worst of the fighting while landing a few good blows. The Ironborn neither respect nor mock you—you're simply not worth their notice."
    }
  }
]"""

DORNE_EVENTS = """[
  {
    "primary_attribute": "Endurance",
    "secondary_attribute": "Cunning",
    "prompt_text": "You must cross the harsh Dornish desert to deliver an urgent message to Sunspear. The heat is merciless, water is scarce, and sand vipers are common.",
    "pass": {
      "message": "You navigate the desert expertly, rationing water and traveling during the cooler hours. You reach Sunspear well ahead of schedule, your message intact."
    },
    "fail": {
      "message": "The desert overwhelms you. Dehydrated and disoriented, you're found by a Dornish patrol and brought to Sunspear, your mission delayed and your reputation damaged."
    },
    "partial_pass": {
      "message": "You reach Sunspear, but barely—exhausted, sunburnt, and days behind schedule. The message is delivered, but your condition raises questions about your capabilities."
    }
  },
  {
    "primary_attribute": "Charisma",
    "secondary_attribute": "Intelligence",
    "prompt_text": "Prince Doran is hosting a feast in Sunspear. You need to gain his ear without attracting attention from those who might oppose your mission.",
    "pass": {
      "message": "You charm your way through the feast, making the right allies and skillfully navigating court etiquette. Prince Doran grants you a private audience, impressed by your diplomacy."
    },
    "fail": {
      "message": "Your attempts to reach Prince Doran are obvious and clumsy. House Martell's guards politely but firmly escort you from the feast, barring your return."
    },
    "partial_pass": {
      "message": "You manage to exchange brief words with Prince Doran during the feast, but in such a public setting, he can only promise to consider your words, not act on them immediately."
    }
  },
  {
    "primary_attribute": "Cunning",
    "secondary_attribute": "Stealth",
    "prompt_text": "You've learned that a conspiracy against your allies is brewing in the Water Gardens. You need to identify the conspirators without revealing your own intentions.",
    "pass": {
      "message": "Through careful observation and subtle manipulation, you uncover the full details of the plot and the identities of all involved, without raising suspicion."
    },
    "fail": {
      "message": "Your investigation is noticed by the conspirators. They feed you false information and use your interest to further their plans, making the situation worse."
    },
    "partial_pass": {
      "message": "You identify some of the conspirators, but sense that key players remain hidden. Your investigation provides useful but incomplete intelligence."
    }
  }
]"""

def setup():
    """Run the full setup process."""
    print("Setting up Game of Thrones Adventure game...")
    
    create_directory_structure()
    write_main_py()
    write_game_map_py()
    write_location_event_files()
    ensure_travel_events()
    
    print("\nSetup complete! To run the game, execute:")
    print("python project_code/src/main.py")


if __name__ == "__main__":
    setup()


# Content for game_map.py
GAME_MAP_PY_CONTENT = """# project_code/src/game_map.py

class GameMap:
    """A map system for the Game of Thrones adventure game."""
    
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
                                 /        \\
                                /          \\
           The Wall -----------+            \\
           /                   |             \\
          /                    |              \\
 Beyond the Wall              /                \\
                             /                  \\
                            /                    \\
                    Winterfell                    \\
                         |                         \\
                         |                          \\
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
                        / \\                     /
                       /   \\                   /
                      /     \\                 /
                Dragonstone  \\               /
                              Highgarden    /
                                    \\      /
                                     \\    /
                                     Dorne
    \"\"\"
        
    def show_map(self):
        """Display the ASCII map with current location marked if set."""
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
        """Set the current team location."""
        if location in self.locations:
            self.current_location = location
            return True
        else:
            return False
            
    def get_available_locations(self):
        """Return list of all game locations with display names."""
        return [self.location_display_names[loc] for loc in self.locations]
        
    def get_current_location(self):
        """Return the current location name."""
        if self.current_location:
            return self.location_display_names[self.current_location]
        return None
"""

# Content for main.py
MAIN_PY_CONTENT = """import json
import sys
import random
import os
from typing import List, Dict, Optional
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


class GameState:
    def __init__(self):
        self.visited_locations = set()  # Tracks unique locations visited
        self.successful_events = 0      # Counts successful events
        self.party = []                 # Reference to the party members


class TravelSystem:
    def __init__(self, travel_events_directory: str):
        self.travel_events = self._load_travel_events(travel_events_directory)
        
    def _load_travel_events(self, directory: str) -> Dict[str, Dict[str, List[TravelEvent]]]:
        """Load all travel events from JSON files in the specified directory."""
        events_by_route = {}
        
        # Check if directory exists
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
            
        print(f"\\nTraveling from {from_location} to {to_location}...\\n")
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
        
        # Initialize game state tracking
        self.game_state = GameState()
        self.game_state.party = self.party

    def start(self):
        # Let the player choose a starting location
        print("Choose a starting location:")
        location_names = list(self.locations.keys())
        for idx, loc_name in enumerate(location_names):
            print(f"{idx + 1}. {self.locations[loc_name].display_name}")
        
        choice = int(self.parser.parse("Enter the number of your starting location: ")) - 1
        self.current_location = location_names[choice]
        
        print(f"\\nYou begin your adventure in {self.locations[self.current_location].display_name}.\\n")
        
        while self.continue_playing:
            self.location_menu()
            
            # Track visited locations
            if self.current_location:
                self.game_state.visited_locations.add(self.current_location)
            
            # Check for game over condition
            if self.check_game_over():
                self.continue_playing = False
        
        print("Game Over.")

    def location_menu(self):
        """Display menu of actions at the current location."""
        location = self.locations[self.current_location]
        
        print(f"\\nYou are in {location.display_name}. What would you like to do?")
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
        
        # Track successful events
        if event.status == EventStatus.PASS:
            self.game_state.successful_events += 1
    
    def travel_menu(self):
        """Display menu of available travel destinations."""
        available_destinations = self.travel_system.get_available_destinations(self.current_location)
        
        if not available_destinations:
            print(f"There are no known routes from {self.locations[self.current_location].display_name}.")
            return
        
        print(f"\\nFrom {self.locations[self.current_location].display_name}, you can travel to:")
        
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
                print(f"\\nYou have arrived at {self.locations[self.current_location].display_name}.\\n")
            else:
                print("\\nYour journey was unsuccessful. You remain at your current location.\\n")
    
    def show_party_status(self):
        """Display status of all party members."""
        print("\\nParty Status:")
        for character in self.party:
            print(f"\\n{character.name}")
            for stat in character.get_stats():
                print(f"  {stat.name}: {stat.value}")
    
    def check_game_over(self):
        """Check if the game should end."""
        return len(self.party) == 0
    
    def display_victory(self):
        """Display victory message when winning conditions are met."""
        print("\\n*********************************************************")
        print("VICTORY! You have successfully completed your adventure!")
        print(f"Locations visited: {len(self.game_state.visited_locations)}")
        print(f"Successful events: {self.game_state.successful_events}")
        print("*********************************************************\\n")


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
        print("\\nGame terminated by user.")
    except Exception as e:
        print(f"\\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    start_game()"""