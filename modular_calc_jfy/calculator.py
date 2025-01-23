import datetime
import re


class InvalidExpressionError(Exception):
    """Given Expression is not valid."""


class Calculator:
    """
    Wrapping simple math functions into Pythons eval    
    """
    
    last_operation = {
                "time": None,
                "input": None,
                "output": None,
            }

    def calc(self, expression: str="") -> float:
        expression = self.__validate_expression(expression)
        evaluated = eval(expression)

        self.last_operation["time"] = datetime.datetime.now()
        self.last_operation["input"] = expression
        self.last_operation["output"] = evaluated

        return float(evaluated)

    @staticmethod
    def __validate_expression(expression: str="") -> str:
        valid_expression_pattern = "^[0-9\.+\-*()/\s]+$"
        
        if re.match(valid_expression_pattern, expression):
            return expression
        raise InvalidExpressionError(f"Invalid Expression, please evaluate syntax:\n{expression}")

    def get_last_operation() -> str:
        return self.last_operation


