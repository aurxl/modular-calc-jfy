import unittest

from modular_calc_jfy.calculator import Calculator, InvalidExpressionError

class Test_Calculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def tearDown(self):
        pass

    def test_calc_simple_calculations(self):
        test_cases = [
                ("1+1", 2.0), 
                ("5.3+2.1", 7.4),
                ("1165+23445", 24610),
                ("3+3+3", 9),
                ("42-42", 0),
                ("42+8-25", 25),
                ("3*3", 9),
                ("(15-5)*3", 30),
                ("25/5", 5),
                ("(100/4)*5", 125),
                ("-100/(-27.5--2.5)", 4)
            ]

        for test_case in test_cases:
            self.assertAlmostEqual(self.calculator.calc(test_case[0]), test_case[1])

    def test_calc_invalid_input(self):
        test_cases = [
                "(1*a)+5=2",
                "[foo]bar",
                "'1+1'",
            ]

        with self.assertRaises(InvalidExpressionError):
            for test_case in test_cases:
                self.calculator.calc(test_case)


