"""
Module 4: Testing - Unittest Examples
---------------------------------------------------------------------
This file demonstrates writing test suites using Python's built-in
`unittest` library, showcasing setup/teardown hooks and standard assertions.
---------------------------------------------------------------------
"""

import unittest

# =====================================================================
# Target Code to Test
# =====================================================================
class SimpleCalculator:
    def add(self, x: float, y: float) -> float:
        return x + y

    def divide(self, x: float, y: float) -> float:
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y


# =====================================================================
# Unittest Test Suite
# =====================================================================
# To use unittest, create a class inheriting from `unittest.TestCase`.

class TestSimpleCalculator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in this class are executed."""
        print("\n--- Starting TestSimpleCalculator Suite ---")
        cls.calc = SimpleCalculator()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in this class are completed."""
        print("--- Completed TestSimpleCalculator Suite ---\n")
        del cls.calc

    def setUp(self):
        """Runs before every individual test method."""
        # Used to set up initial state
        self.message = "Running single test execution"

    def tearDown(self):
        """Runs after every individual test method."""
        # Used for cleanup operations
        pass

    # Note: Test method names must begin with the prefix `test_`
    def test_addition(self):
        print(f"[{self._testMethodName}]: {self.message}")
        result = self.calc.add(10.5, 4.5)
        # Standard Assertion
        self.assertEqual(result, 15.0)

    def test_division(self):
        print(f"[{self._testMethodName}]: {self.message}")
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_division_by_zero_raises_error(self):
        print(f"[{self._testMethodName}]: {self.message}")
        # Assert exception is raised
        with self.assertRaises(ZeroDivisionError) as context:
            self.calc.divide(5, 0)
        
        # Verify the exception message
        self.assertEqual(str(context.exception), "Cannot divide by zero.")

    def test_boolean_assertions(self):
        print(f"[{self._testMethodName}]: {self.message}")
        # Demonstrating other assertion helpers
        self.assertTrue(5 > 3)
        self.assertFalse(3 > 5)
        self.assertIsNotNone(self.calc)


# =====================================================================
# Organizing Test Suites Programmatically
# =====================================================================
def suite():
    """Builds a test suite programmatically."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestSimpleCalculator('test_addition'))
    test_suite.addTest(TestSimpleCalculator('test_division'))
    return test_suite


if __name__ == "__main__":
    # Runs all tests in this file
    unittest.main()
