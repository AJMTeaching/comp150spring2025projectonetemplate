# Game of Thrones Adventure

A text-based adventure game set in the world of Westeros and beyond. Navigate through iconic locations from the series, encounter challenges, and make choices that will determine your fate in the Seven Kingdoms.

## Table of Contents
- [Installation](#installation)
- [Game Overview](#game-overview)
- [How to Play](#how-to-play)
- [Character Skills](#character-skills)
- [Locations](#locations)
- [Events & Challenges](#events--challenges)
- [Travel System](#travel-system)
- [Tips for Success](#tips-for-success)
- [Development](#development)
- [Contributing](#contributing)

## Installation

### Prerequisites
- Python 3.12.6 or higher

### Option 1: Clone the Repository
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/got-adventure.git
   cd got-adventure
   ```

2. Run the game:
   ```bash
   python project_code/src/main.py
   ```

### Option 2: Install via Pip
1. Install the game package:
   ```bash
   pip install adventure-game
   ```

2. Launch the game:
   ```bash
   adventure-game
   ```

## Game Overview

In Game of Thrones Adventure, you control a party of characters navigating through the dangerous world of Westeros. Your party begins with three characters: Arya, Jon, and Tyrion, each with unique strengths and weaknesses.

The game is entirely text-based and played through terminal/command line input. You'll face events and challenges at various locations across the Seven Kingdoms and beyond, making decisions that impact your journey and determine whether you succeed or fail.

## How to Play

1. **Starting the Game**: When you launch the game, you'll be prompted to choose a starting location.

2. **Location Menu**: At each location, you'll see a menu with the following options:
   - Explore this location
   - Travel to another location
   - View party status
   - Quit game

3. **Exploration**: When exploring a location, you'll encounter random events specific to that area.

4. **Events**: For each event, you'll need to:
   - Choose a character from your party to handle the situation
   - Select which of their skills to use
   
5. **Outcomes**: Based on your choices, one of three outcomes will occur:
   - **Success** (Pass): The character used the primary skill required for the event
   - **Partial Success** (Partial Pass): The character used the secondary skill
   - **Failure** (Fail): The character used a skill not suited for the event

6. **Travel**: To move between locations, select "Travel to another location" from the menu. You'll face travel events between locations that work the same way as location events.

## Character Skills

Each character has six key skills that determine their effectiveness in different situations:

- **Strength**: Physical power and combat prowess
- **Intelligence**: Problem-solving and knowledge
- **Charisma**: Social influence and persuasion
- **Stealth**: Ability to move unseen and unheard
- **Cunning**: Cleverness, deception, and strategizing
- **Endurance**: Stamina, resilience, and survival

Characters have different starting values for these skills:

### Arya
- Specializes in Stealth
- Good Intelligence
- Decent Strength

### Jon
- Specializes in Strength and Endurance
- Decent Charisma

### Tyrion
- Specializes in Intelligence and Cunning
- Good Charisma

## Locations

The game features multiple iconic locations from Game of Thrones:

- Winterfell
- King's Landing
- The Wall
- Beyond the Wall
- The Eyrie
- The Iron Islands
- Dragonstone
- Braavos
- Dorne

Each location has unique events and challenges themed to that area.

## Events & Challenges

Events are scenario-based challenges that require specific skills to overcome. Each event has:

- A primary skill (best outcome)
- A secondary skill (partial success)
- A description of the challenge
- Three possible outcomes (pass, partial pass, or fail)

Examples include:
- Deciphering secret messages at the Wall
- Navigating court politics in King's Landing
- Surviving harsh environmental conditions beyond the Wall

## Travel System

Traveling between locations triggers travel events, which function similarly to location events. Successfully overcoming a travel event allows you to reach your destination, while failure might prevent your journey or have other negative consequences.

## Tips for Success

1. **Choose the Right Character**: Different characters excel at different skills. Use Arya for stealth challenges, Jon for strength and endurance, and Tyrion for intelligence and social situations.

2. **Read Carefully**: Event descriptions often contain clues about which skills might be most effective.

3. **Balance Exploration and Travel**: Explore each location thoroughly before moving on to discover all the unique events and potential rewards.

4. **Manage Your Party**: Keep track of each character's strengths and use them strategically for different challenges.

## Development

This game was developed as part of COMP150 Spring 2025. The codebase uses Python's object-oriented features to create a modular, extensible game engine.

### Project Structure
```
.
├── project_code/
│   ├── location_events/        # JSON files for location events
│   ├── travel_events/          # JSON files for travel events 
│   ├── src/                    # Source code
│   │   ├── main.py             # Main game code
│   │   ├── travel_system.py    # Travel mechanics
│   │   └── game_map.py         # Map system
│   └── test/                   # Unit tests
├── README.md                   # This file
└── setup.py                    # Installation configuration
```

### Running Tests

To run the unit tests:

```bash
python -m unittest discover project_code/test
```

## Contributing

This project is part of a course assignment, but suggestions and bug reports are welcome! Please open an issue on the repository if you encounter any problems or have ideas for improvements.

---

Enjoy your adventure in the world of Game of Thrones! Remember, when you play the game of thrones, you win or you die. There is no middle ground.
