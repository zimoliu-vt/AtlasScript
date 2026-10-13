
from dataclasses import dataclass
from atlasscript.lexer import tokenize


# AST node definitions

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
class Assign:
    name: str
    value: object


@dataclass
class Print:
    value: object


@dataclass
class If:
    condition: object
    then_body: list
    else_body: list


@dataclass
class While:
    condition: object
    body: list


@dataclass
class Function:
    name: str
    params: list
    body: list


@dataclass
class Call:
    name: str
    args: list


@dataclass
class Return:
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

    def block(self):
        self.expect("{")
        statements = []

        while self.current().value != "}":
            if self.current().kind == "EOF":
                raise SyntaxError("Unterminated block")
            statements.append(self.statement())

        self.expect("}")
        return statements

    def statement(self):

        
        if self.match("fn"):
            name = self.current()

            if name.kind != "IDENTIFIER":
                raise SyntaxError("Expected function name")

            self.pos += 1
            self.expect("(")

            params = []

            if self.current().value != ")":
                while True:
                    param = self.current()

                    if param.kind != "IDENTIFIER":
                        raise SyntaxError(
                            "Expected parameter name"
                        )

                    params.append(param.value)
                    self.pos += 1

                    if not self.match(","):
                        break

            self.expect(")")
            body = self.block()

            if len(params) != len(set(params)):
                raise SyntaxError("Duplicate parameter name")

            return Function(name.value, params, body)

        if self.match("return"):
            value = self.expression()
            self.expect(";")
            return Return(value)


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

        if self.match("if"):
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            then_body = self.block()

            else_body = []
            if self.match("else"):
                else_body = self.block()

            return If(condition, then_body, else_body)

        if self.match("while"):
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            body = self.block()
            return While(condition, body)

        if self.current().kind == "IDENTIFIER":
            name = self.current().value
            self.pos += 1
            self.expect("=")
            value = self.expression()
            self.expect(";")
            return Assign(name, value)

        raise SyntaxError(
            f"Unexpected statement at "
            f"position {self.current().position}"
        )

    def expression(self):
        return self.equality()

    def equality(self):
        node = self.comparison()

        while self.current().value in ("==", "!="):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.comparison())

        return node

    def comparison(self):
        node = self.term()

        while self.current().value in ("<", ">", "<=", ">="):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current().value in ("+", "-"):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.factor())

        return node

    def factor(self):
        node = self.primary()

        while self.current().value in ("*", "/"):
            op = self.current().value
            self.pos += 1
            node = Binary(node, op, self.primary())

        return node

    def primary(self):
        token = self.current()

        if token.kind == "NUMBER":
            self.pos += 1
            return Number(int(token.value))

        if token.kind == "STRING":
            self.pos += 1
            return String(token.value)

        
        if token.kind == "IDENTIFIER":
            self.pos += 1

            if self.match("("):
                args = []

                if self.current().value != ")":
                    while True:
                        args.append(self.expression())

                        if not self.match(","):
                            break

                self.expect(")")
                return Call(token.value, args)

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
