**Welcome!!**
## How to Run the Project 

To run the example project, follow the steps below:

### Prerequisites
- Python 3.12.6 installed on your machine.

### Steps to Run

1. Clone or download the project to your local machine.

2. Navigate to the project root directory (assumed to be named `comp150spring2025projectonetemplate`):

   ```bash
   cd comp150spring2025projectonetemplate
   ```

3. Run the game using Python:

   ```bash
   python project_code/src/main.py
   ```

### Game Flow

- The game will prompt you to select a party member and choose a statistic (e.g., Strength or Intelligence) to resolve various in-game events.
- Follow the instructions displayed in the terminal to play through the game.

### Example

After running the game, you will see a series of prompts like:

```
A mysterious door blocks your path, with a riddle inscribed. What will you do?

Choose a party member:
1. Character_0
2. Character_1
3. Character_2

Enter the number of the chosen party member: 
```

Simply follow the prompts to make your choices and see the outcomes.

### Running Unit Tests

To run the provided unit tests, we recommend using `pytest`, a testing framework for Python.

#### Steps to Run Tests:

1. First, make sure `pytest` is installed on your machine:

   ```bash
   pip install pytest
   ```

2. Run the tests by navigating to the project root and executing the following command:

   ```bash
   pytest
   ```

This will discover and run all the tests in the `test/` directory.

### Example Test Output:

After running the tests, you should see output like this:

```
============================= test session starts ==============================
collected 3 items

test/test_game.py ...                                                     [100%]

============================== 3 passed in 0.05s ===============================
```

### Project Structure

Here is the project directory structure:

```
.
adventure-game/                      # Root directory of your repository
├── README.md                        # Project documentation (at root)
├── requirements.txt                 # Python dependencies (at root)
├── setup.py                         # Installation configuration (at root)
├── adventure_game/                  # Main package directory
│   ├── __init__.py
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── game_map.py
│   │   ├── travel_system.py
│   │   └── character_system.py
│   ├── location_events/
│   │   ├── __init__.py
│   │   └── ... (json files)
│   ├── travel_events/
│   │   ├── __init__.py
│   │   └── ... (json files)
│   └── test/
│       ├── __init__.py
│       └── ... (test files)
```

- `project_code/` - The main directory containing all the code for the project.
    - `location_events/` - Directory containing the JSON files with events for the game.
    - `src/` - Source code for the project.
    - `test/` - Directory for tests to ensure the game functions correctly.
- `README1.md` - This file, with instructions on how to run the project.
- `PROJECT_INSTRUCTIONS.md` - Additional instructions or guidelines for the project.

---

Have Fun!!

