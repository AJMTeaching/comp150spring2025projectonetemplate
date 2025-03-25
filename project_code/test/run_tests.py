#!/usr/bin/env python3
"""
Test runner for the Game of Thrones Adventure game.
Discovers and runs all tests in the test directory.
"""

import unittest
import sys
import os

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

def run_tests():
    """Discover and run all tests in the test directory."""
    print("Running Game of Thrones Adventure tests...")
    
    # Discover all tests in the project_code/test directory
    test_loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_suite = test_loader.discover(test_dir)
    
    # Create a test runner and run the discovered tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    results = test_runner.run(test_suite)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Ran {results.testsRun} tests")
    print(f"Failures: {len(results.failures)}")
    print(f"Errors: {len(results.errors)}")
    print(f"Skipped: {len(results.skipped)}")
    
    # Return True if all tests passed, False otherwise
    return len(results.failures) == 0 and len(results.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
