Game of Thrones Adventure
A text-based adventure game set in the world of Westeros and beyond. Navigate through iconic locations from the series, encounter challenges, and make choices that will determine your fate in the Seven Kingdoms.
Table of Contents

Installation
Game Overview
How to Play
Character Skills
Locations
Events & Challenges
Travel System
Tips for Success
Development
Contributing

Installation
Prerequisites

Python 3.12.6 or higher

Option 1: Clone the Repository

Clone this repository to your local machine:
bashCopygit clone https://github.com/yourusername/got-adventure.git
cd got-adventure

Run the game:
bashCopypython -m project_code.src.main


Option 2: Install via Pip

Install the game package:
bashCopypip install got-adventure

Launch the game:
bashCopygot-adventure


Game Overview
In Game of Thrones Adventure, you control a party of characters navigating through the dangerous world of Westeros. Your party begins with three characters: Arya, Jon, and Tyrion, each with unique strengths and weaknesses.
The game is entirely text-based and played through terminal/command line input. You'll face events and challenges at various locations across the Seven Kingdoms and beyond, making decisions that impact your journey and determine whether you succeed or fail.
How to Play

Starting the Game: When you launch the game, you'll be prompted to choose a starting location from the list presented.
Location Menu: At each location, you'll see a menu with the following options:

Explore this location: Encounter a random event specific to your current location
Travel to another location: Move to a different area of Westeros (triggers travel events)
View party status: Check the current skills and abilities of your characters
Quit game: Exit the game


Event Challenges: When you explore a location or travel, you'll encounter events that require you to:

Choose a character from your party to handle the situation
Select which of their skills to use for the challenge


Making Choices: Read event descriptions carefully - they often contain hints about which skills would be most effective! If you enter an invalid choice, the game will prompt you to try again.
Event Outcomes: Based on your character and skill choices, one of three outcomes will occur:

Success: Your character used the primary skill required for the event
Partial Success: Your character used the secondary skill that partially addresses the challenge
Failure: Your character used a skill not suited for the event


Travel: When you choose to travel to another location, you'll see a list of available destinations. After selecting one, you'll face a travel event that works the same way as location events. If you fail a travel event, you'll remain at your current location.

Character Skills
Each character has six key skills that determine their effectiveness in different situations:

Strength: Physical power and combat prowess
Intelligence: Problem-solving and knowledge
Charisma: Social influence and persuasion
Stealth: Ability to move unseen and unheard
Cunning: Cleverness, deception, and strategizing
Endurance: Stamina, resilience, and survival

Character Specialties
Each character has different starting values for these skills, making them better suited for certain challenges:
Arya Stark

Specialties: Stealth (80), Intelligence (65)
Decent: Strength (60)
Other skills start at 50

Jon Snow

Specialties: Strength (75), Endurance (70)
Decent: Charisma (60)
Other skills start at 50

Tyrion Lannister

Specialties: Intelligence (85), Cunning (80)
Decent: Charisma (75)
Other skills start at 50

Locations
The game features multiple iconic locations from Game of Thrones, each with unique events:

Winterfell: Ancestral home of House Stark
King's Landing: Capital of the Seven Kingdoms
The Wall: Massive ice structure defending the realm
Beyond the Wall: The dangerous frozen lands of the far north
The Eyrie: Impregnable mountain fortress of House Arryn
The Iron Islands: Home of the seafaring Ironborn
Dragonstone: Ancient Targaryen stronghold
Braavos: Free city across the Narrow Sea
Dorne: The southernmost kingdom, known for its independence

Events & Challenges
Events are scenario-based challenges that test your characters' skills. Each event has:

A primary skill (for best outcome)
A secondary skill (for partial success)
A narrative description of the challenge
Three possible outcomes (success, partial success, or failure)

Examples include:

Deciphering messages at the Wall (Intelligence)
Navigating court politics in King's Landing (Cunning/Charisma)
Surviving harsh weather beyond the Wall (Endurance)
Sneaking into forbidden areas (Stealth)

Travel System
Traveling between locations triggers travel events with their own challenges. Successfully overcoming a travel event allows you to reach your destination, while failure means you must remain at your current location and try again. Each journey presents different challenges based on the route.
Tips for Success

Match Characters to Challenges: Use Arya for stealth challenges, Jon for strength and endurance tests, and Tyrion for intelligence and social situations.
Read Carefully: Event descriptions often contain clues about which skills might be most effective.
Balance Exploration and Travel: Thoroughly explore each location before moving on to discover all the unique events and potential story elements.
Be Strategic: If you fail at traveling to a new location, consider exploring your current location more or trying a different character or skill combination.
Learn from Failures: Even failed events provide information about the world and what skills might work better next time.

Development
This game was developed as part of COMP150 Spring 2025. The codebase uses Python's object-oriented features to create a modular, extensible game engine.
Project Structure
Copy.
├── project_code/
│   ├── location_events/        # JSON files for location events
│   ├── travel_events/          # JSON files for travel events 
│   ├── src/                    # Source code
│   │   ├── main.py             # Main game code
│   │   ├── model.py            # Game models
│   │   ├── travel_system.py    # Travel mechanics
│   │   └── game_map.py         # Map system
│   └── test/                   # Unit tests
├── README.md                   # This file
└── setup.py                    # Installation configuration
Running Tests
To run the unit tests:
bashCopypython -m unittest discover project_code/test
Contributing
This project is part of a course assignment, but suggestions and bug reports are welcome! Please open an issue on the repository if you encounter any problems or have ideas for improvements.

Enjoy your adventure in the world of Game of Thrones! Remember, when you play the game of thrones, you win or you die. There is no middle ground.
