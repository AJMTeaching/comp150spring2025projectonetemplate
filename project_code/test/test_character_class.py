import sys
import os
import unittest
from unittest.mock import patch

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Character, Statistic

class TestCharacter(unittest.TestCase):
    """Test the Character class and its methods."""
    
    def setUp(self):
        """Initialize test character before each test."""
        self.character = Character("Daenerys Targaryen")
    
    def test_character_initialization(self):
        """Test that a character is correctly initialized with default stats."""
        self.assertEqual(self.character.name, "Daenerys Targaryen")
        self.assertEqual(self.character.strength.value, 50)
        self.assertEqual(self.character.intelligence.value, 50)
        self.assertEqual(self.character.charisma.value, 50)
        self.assertEqual(self.character.stealth.value, 50)
        self.assertEqual(self.character.cunning.value, 50)
        self.assertEqual(self.character.endurance.value, 50)
    
    def test_character_get_stats(self):
        """Test that get_stats returns all character statistics."""
        stats = self.character.get_stats()
        self.assertEqual(len(stats), 6)  # Character should have 6 stats
        
        # Check that all stats are instances of Statistic
        for stat in stats:
            self.assertIsInstance(stat, Statistic)
        
        # Verify specific stats are included
        stat_names = [stat.name for stat in stats]
        self.assertIn("Strength", stat_names)
        self.assertIn("Intelligence", stat_names)
        self.assertIn("Charisma", stat_names)
        self.assertIn("Stealth", stat_names)
        self.assertIn("Cunning", stat_names)
        self.assertIn("Endurance", stat_names)
    
    def test_character_str_representation(self):
        """Test the string representation of a character."""
        char_str = str(self.character)
        self.assertIn("Daenerys Targaryen", char_str)
        self.assertIn("Strength", char_str)
        self.assertIn("Intelligence", char_str)
    
    def test_modify_character_stats(self):
        """Test that character stats can be modified."""
        # Modify stats
        self.character.strength.value = 75
        self.character.intelligence.value = 85
        
        self.assertEqual(self.character.strength.value, 75)
        self.assertEqual(self.character.intelligence.value, 85)
        
        # Test modification through the modify method
        self.character.strength.modify(10)
        self.character.intelligence.modify(-15)
        
        self.assertEqual(self.character.strength.value, 85)
        self.assertEqual(self.character.intelligence.value, 70)
    
    def test_character_with_max_stats(self):
        """Test a character with maximum stats."""
        max_char = Character("Max Stats")
        for stat in max_char.get_stats():
            stat.value = 100
        
        for stat in max_char.get_stats():
            self.assertEqual(stat.value, 100)
            
        # Test that stats don't exceed maximum
        for stat in max_char.get_stats():
            stat.modify(20)
            self.assertEqual(stat.value, 100)
    
    def test_character_with_min_stats(self):
        """Test a character with minimum stats."""
        min_char = Character("Min Stats")
        for stat in min_char.get_stats():
            stat.value = 0
        
        for stat in min_char.get_stats():
            self.assertEqual(stat.value, 0)
            
        # Test that stats don't go below minimum
        for stat in min_char.get_stats():
            stat.modify(-20)
            self.assertEqual(stat.value, 0)

if __name__ == '__main__':
    unittest.main()
