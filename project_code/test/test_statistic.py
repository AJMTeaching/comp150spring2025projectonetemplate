import sys
import os
import unittest

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from project_code.src.main import Statistic

class TestStatistic(unittest.TestCase):
    """Test the Statistic class and its methods."""
    
    def setUp(self):
        """Initialize test statistics before each test."""
        self.default_stat = Statistic("Default")
        self.custom_stat = Statistic(
            name="Wisdom", 
            value=75, 
            description="Knowledge and good judgment", 
            min_value=10, 
            max_value=120
        )
    
    def test_default_initialization(self):
        """Test statistics initialized with default values."""
        self.assertEqual(self.default_stat.name, "Default")
        self.assertEqual(self.default_stat.value, 0)
        self.assertEqual(self.default_stat.description, "")
        self.assertEqual(self.default_stat.min_value, 0)
        self.assertEqual(self.default_stat.max_value, 100)
    
    def test_custom_initialization(self):
        """Test statistics initialized with custom values."""
        self.assertEqual(self.custom_stat.name, "Wisdom")
        self.assertEqual(self.custom_stat.value, 75)
        self.assertEqual(self.custom_stat.description, "Knowledge and good judgment")
        self.assertEqual(self.custom_stat.min_value, 10)
        self.assertEqual(self.custom_stat.max_value, 120)
    
    def test_str_representation(self):
        """Test the string representation of a statistic."""
        self.assertEqual(str(self.default_stat), "Default: 0")
        self.assertEqual(str(self.custom_stat), "Wisdom: 75")
    
    def test_modify_within_bounds(self):
        """Test modifying a statistic within bounds."""
        # Increase value
        self.default_stat.modify(25)
        self.assertEqual(self.default_stat.value, 25)
        
        # Decrease value
        self.default_stat.modify(-10)
        self.assertEqual(self.default_stat.value, 15)
    
    def test_modify_beyond_max(self):
        """Test modifying a statistic beyond maximum value."""
        self.default_stat.value = 90
        self.default_stat.modify(20)
        self.assertEqual(self.default_stat.value, 100)
    
    def test_modify_below_min(self):
        """Test modifying a statistic below minimum value."""
        self.default_stat.value = 10
        self.default_stat.modify(-20)
        self.assertEqual(self.default_stat.value, 0)
    
    def test_custom_bounds(self):
        """Test modifying a statistic with custom min/max bounds."""
        # Test pushing beyond max
        self.custom_stat.modify(50)
        self.assertEqual(self.custom_stat.value, 120)
        
        # Test pushing below min
        self.custom_stat.modify(-200)
        self.assertEqual(self.custom_stat.value, 10)
    
    def test_zero_modification(self):
        """Test modifying a statistic by zero."""
        initial_value = self.custom_stat.value
        self.custom_stat.modify(0)
        self.assertEqual(self.custom_stat.value, initial_value)

if __name__ == '__main__':
    unittest.main()
