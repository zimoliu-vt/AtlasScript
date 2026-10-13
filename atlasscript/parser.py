
from dataclasses import dataclass
from atlasscript.lexer import tokenize


@dataclass
class Number:
    value: int


@dataclass
class String:
    value: str


@dataclass
class Variable:
    name: str


@dataclass
class Binary:
    left: object
    operator: str
    right: object


@dataclass
class Let:
    name: str
    value: object


@dataclass
class Print:
    value: object


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def match(self, value):
        if self.current().value == value:
            self.pos += 1
            return True
        return False

    def expect(self, value):
        if not self.match(value):
            raise SyntaxError(
                f"Expected {value!r} at "
                f"position {self.current().position}"
            )

    def parse(self):
        statements = []

        while self.current().kind != "EOF":
            statements.append(self.statement())

        return statements

    def statement(self):
        if self.match("let"):
            name = self.current()

            if name.kind != "IDENTIFIER":
                raise SyntaxError("Expected variable name")

            self.pos += 1
            self.expect("=")
            value = self.expression()
            self.expect(";")

            return Let(name.value, value)

        if self.match("print"):
            self.expect("(")
            value = self.expression()
            self.expect(")")
            self.expect(";")

            return Print(value)

        raise SyntaxError(
            f"Unexpected statement at "
            f"position {self.current().position}"
        )

    def expression(self):
        node = self.term()

        while self.current().value in ("+", "-"):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current().value in ("*", "/"):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.factor())

        return node

    def factor(self):
        token = self.current()

        if token.kind == "NUMBER":
            self.pos += 1
            return Number(int(token.value))

        if token.kind == "STRING":
            self.pos += 1
            return String(token.value)

        if token.kind == "IDENTIFIER":
            self.pos += 1
            return Variable(token.value)

        if self.match("("):
            node = self.expression()
            self.expect(")")
            return node

        raise SyntaxError(
            f"Unexpected token at position {token.position}"
        )


def parse(source):
    return Parser(tokenize(source)).parse()
