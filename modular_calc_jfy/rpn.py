from operator import add, sub, mul, truediv
import re

class ReversePolishNotation:
    """
    Implementing the Shunting Yard Algorithm to build a reverse polish notation
    from an infix notation. And provide an eval function for that.

    https://en.wikipedia.org/wiki/Shunting_yard_algorithm
    """

    # Define the precedence of supported Operators.
    precedence = {
        "+": 0,
        "-": 1,
        "*": 2,
        "/": 3,
    }

    def __is_number(num:str) -> bool:
        try:
            float(num)
            return True
        except ValueError:
            return False

    @classmethod
    def build(cls, expr:str) -> list:
        """
        Build from a given expression in infix notation a reverse polish notation
        in postfix notation.
        
        See:
          https://en.wikipedia.org/wiki/Shunting_yard_algorithm#The_algorithm_in_detail
        for the pseudocode example.
        """
        tokens = re.findall('[0-9]+[.]?[0-9]+|[0-9]+|[+\-*\/()]', expr)
        output_queue = []
        operator_stack = []

        for token in tokens:
            if cls.__is_number(token):
                output_queue.append(token)
            elif token in cls.precedence:
                while operator_stack and cls.precedence.get(operator_stack[-1], -1) >= cls.precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
        while operator_stack:
            output_queue.append(operator_stack.pop())
    
        return output_queue

    @classmethod
    def eval(cls, rpn:list) -> float:
        """
        Provide an evaluator for the reverse polish notation.

        Pretty straight forward, pop numbers from the rpn onto the
        eval_stack, till an operator is found. Apply that operator 
        to the last two at the eval_stack and put that number back
        on top. REPEAT.
        """
        eval_stack = []

        for token in rpn:
            if cls.__is_number(token):
                eval_stack.append(token)
            elif token in cls.precedence:
                right = float(eval_stack.pop())
                left = float(eval_stack.pop())
                if token == "+": eval_stack.append(add(left, right))
                if token == "-": eval_stack.append(sub(left, right))
                if token == "*": eval_stack.append(mul(left, right))
                if token == "/": eval_stack.append(truediv(left, right))

        return eval_stack[0]

    @classmethod
    def calc(cls, expr:str):
        """Wrapping build and eval for easy use."""
        return cls.eval(cls.build(expr))


if __name__ == "__main__":
    expr = "1+1"
    rpn = ReversePolishNotation.build(expr)
    print(f"rpn: {ReversePolishNotation.eval(rpn)}")
    print(f"eval: {eval(expr)}")
