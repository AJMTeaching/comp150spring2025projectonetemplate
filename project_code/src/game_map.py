# project_code/src/game_map.py

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
        self.map_ascii = """
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
        """
        
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
