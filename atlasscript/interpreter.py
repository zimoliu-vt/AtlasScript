
from atlasscript.parser import (
    Number, String, Variable, Binary, Let, Print
)


class Interpreter:
    def __init__(self):
        # Stores AtlasScript variables.
        self.variables = {}

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

            raise RuntimeError(
                f"Unknown operator: {node.operator}"
            )

        raise RuntimeError(
            f"Unknown expression: {node}"
        )

    def execute(self, statement):
        if isinstance(statement, Let):
            value = self.evaluate(statement.value)
            self.variables[statement.name] = value
            return

        if isinstance(statement, Print):
            value = self.evaluate(statement.value)
            print(value)
            return

        raise RuntimeError(
            f"Unknown statement: {statement}"
        )

    def run(self, statements):
        for statement in statements:
            self.execute(statement)
