
from dataclasses import dataclass


@dataclass
class Token:
    kind: str
    value: str
    position: int


KEYWORDS = {"let", "fn", "return", "if", "else", "while"}


def tokenize(source: str) -> list[Token]:
    tokens = []
    i = 0

    while i < len(source):
        char = source[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit():
            start = i
            while i < len(source) and source[i].isdigit():
                i += 1
            tokens.append(Token("NUMBER", source[start:i], start))
            continue

        if char.isalpha() or char == "_":
            start = i
            while i < len(source) and (
                source[i].isalnum() or source[i] == "_"
            ):
                i += 1

            word = source[start:i]
            kind = "KEYWORD" if word in KEYWORDS else "IDENTIFIER"
            tokens.append(Token(kind, word, start))
            continue

        if char == '"':
            start = i
            i += 1
            value_start = i

            while i < len(source) and source[i] != '"':
                i += 1

            if i >= len(source):
                raise SyntaxError(
                    f"Unterminated string at position {start}"
                )

            tokens.append(
                Token("STRING", source[value_start:i], start)
            )
            i += 1
            continue

        if char in "+-*/=(){};,":
            tokens.append(Token("SYMBOL", char, i))
            i += 1
            continue

        raise SyntaxError(
            f"Unexpected character {char!r} at position {i}"
        )

    tokens.append(Token("EOF", "", len(source)))
    return tokens
