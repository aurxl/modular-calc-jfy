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
        "-u": 4, # The negative unary operator
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

        It is modyfied so that unary operators can be handled. Unary Operators are
        either after another operator, at the start of an expression or after '('
        open bracket. Unary operators have the highest priority to be associated with
        the last number in queue.
        """
        tokens = re.findall('[0-9]+[.]?[0-9]+|[0-9]+|[+\\-*\\/()]', expr)
        output_queue = []
        operator_stack = []
        unary_condition = True

        for i, token in enumerate(tokens):
            if cls.__is_number(token):
                output_queue.append(token)
                unary_condition = False
            elif token in cls.precedence:
                if unary_condition:
                    token = "-u"
                while operator_stack and cls.precedence.get(operator_stack[-1], -1) >= cls.precedence[token]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                unary_condition = True
            elif token == "(":
                if output_queue and cls.__is_number(tokens[i-1]):
                    operator_stack.append("*")
                operator_stack.append(token)
                unary_condition = True
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
                unary_condition = False
                if i+1 != len(tokens):
                    if cls.__is_number(tokens[i+1]) or tokens[i+1] == "(":
                        while operator_stack and cls.precedence.get(operator_stack[-1], -1) >= cls.precedence["*"]:
                            output_queue.append(operator_stack.pop())
                        operator_stack.append("*")
            else:
                raise ValueError(f"Unexpected token {token}.")
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
        on top. When Operator is unary, then multiply last item on
        stack with -1. REPEAT.
        """
        eval_stack = []

        for token in rpn:
            if cls.__is_number(token):
                eval_stack.append(token)
            elif token in cls.precedence:
                right = float(eval_stack.pop())

                if token == "-u":
                    eval_stack.append(mul(-1, right))
                    continue

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
    expr = "5(30-5)"
    rpn = ReversePolishNotation.build(expr)

    print(f"rpn: {''.join(rpn)}")
    print(f"rpn eval:    {ReversePolishNotation.eval(rpn)}")
    print(f"python eval: {eval(expr)}")
