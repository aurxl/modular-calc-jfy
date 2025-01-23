import unittest

from modular_calc_jfy.calculator import Calculator

class Test_Calculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def tearDown(self):
        pass

    def test_calc_simple_addition(self):
        test_cases = [
                ("1+1", "2"), 
                ("5+2", "7"),
                ("1165+23445", "24610")
                ]

        for test_case in test_cases:
            self.assertEqual(self.calculator.calc(test_case[0]), test_case[1])

    def test_calc_invalid_input(self):
        pass

    def test_calc_multiple_addition(self):
        pass


