#!/usr/bin/env python3
"""
Test runner for the AI Engineer Assignment
"""
import unittest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Run all tests in the tests directory"""
    
    # Discover and run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # Run tests with verbose output
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Print summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    
    print(f"\n{'='*60}")
    print(f"Tests run: {tests_run}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)