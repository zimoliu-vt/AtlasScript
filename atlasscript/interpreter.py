
from atlasscript.parser import (
    Number, String, Variable, Binary,
    Let, Assign, Print, If, While,
    Function, Call, Return
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.call_stack = []
        self.max_call_depth = 100

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, String):
            return node.value

        if isinstance(node, Variable):
            if node.name not in self.variables:
                raise NameError(
                    f"Undefined variable: {node.name}"
                )
            return self.variables[node.name]

        if isinstance(node, Binary):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.operator == "+":
                return left + right
            if node.operator == "-":
                return left - right
            if node.operator == "*":
                return left * right
            if node.operator == "/":
                if right == 0:
                    raise ZeroDivisionError(
                        "Cannot divide by zero"
                    )
                return left / right

            if node.operator == "==":
                return left == right
            if node.operator == "!=":
                return left != right
            if node.operator == "<":
                return left < right
            if node.operator == ">":
                return left > right
            if node.operator == "<=":
                return left <= right
            if node.operator == ">=":
                return left >= right

            raise RuntimeError(
                f"Unknown operator: {node.operator}"
            )

        if isinstance(node, Call):
            if node.name not in self.functions:
                raise NameError(
                    f"Undefined function: {node.name}"
                )

            function = self.functions[node.name]

            if len(node.args) != len(function.params):
                raise TypeError(
                    f"{node.name} expects "
                    f"{len(function.params)} arguments, "
                    f"got {len(node.args)}"
                )

            args = [
                self.evaluate(arg)
                for arg in node.args
            ]

            if len(self.call_stack) >= self.max_call_depth:
                raise RuntimeError(
                    "Maximum call depth exceeded"
                )

            previous_variables = self.variables
            local_variables = dict(
                zip(function.params, args)
            )

            self.call_stack.append(node.name)
            self.variables = local_variables

            try:
                self.run(function.body)
            except ReturnSignal as signal:
                return signal.value
            finally:
                self.variables = previous_variables
                self.call_stack.pop()

            return None

        raise RuntimeError(
            f"Unknown expression: {node}"
        )

    def execute(self, statement):
        if isinstance(statement, Let):
            self.variables[statement.name] = self.evaluate(
                statement.value
            )
            return

        if isinstance(statement, Assign):
            if statement.name not in self.variables:
                raise NameError(
                    f"Undefined variable: {statement.name}"
                )

            self.variables[statement.name] = self.evaluate(
                statement.value
            )
            return

        if isinstance(statement, Print):
            print(self.evaluate(statement.value))
            return

        if isinstance(statement, If):
            body = (
                statement.then_body
                if self.evaluate(statement.condition)
                else statement.else_body
            )
            self.run(body)
            return

        if isinstance(statement, While):
            while self.evaluate(statement.condition):
                self.run(statement.body)
            return

        if isinstance(statement, Function):
            self.functions[statement.name] = statement
            return

        if isinstance(statement, Return):
            if not self.call_stack:
                raise RuntimeError(
                    "return outside a function"
                )

            raise ReturnSignal(
                self.evaluate(statement.value)
            )

        raise RuntimeError(
            f"Unknown statement: {statement}"
        )

    def run(self, statements):
        for statement in statements:
            self.execute(statement)
