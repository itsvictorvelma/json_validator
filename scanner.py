from enum import StrEnum, auto
from typing import Any


class TokenType(StrEnum):
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()

    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    COLON = auto()
    EOF = auto()


class Token:
    token_type: TokenType
    value: Any
    line: int

    def __init__(self, token_type: TokenType, value: Any, line: int = 1):
        self.token_type = token_type
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Token({self.token_type}, {self.value!r}, line={self.line})"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens: list[Token] = []

    def scan(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case "{":
                self.add_token(TokenType.LEFT_BRACE, c)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE, c)
            case "[":
                self.add_token(TokenType.LEFT_BRACKET, c)
            case "]":
                self.add_token(TokenType.RIGHT_BRACKET, c)
            case ",":
                self.add_token(TokenType.COMMA, c)
            case ":":
                self.add_token(TokenType.COLON, c)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.add_string()
            case "-":
                if self.peek().isdigit():
                    self.add_number()
                else:
                    raise ValueError(f"Line {self.line}: '-' must be followed by a digit")
            case _:
                if c.isdigit():
                    self.add_number()
                elif c.isalpha():
                    self.add_keyword()
                else:
                    raise ValueError(f"Line {self.line}: unexpected character {c!r}")

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def peek(self) -> str:
        if self.is_at_end():
            return ""
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return ""
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, value: Any) -> None:
        self.tokens.append(Token(token_type, value, self.line))

    def add_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise ValueError(f"Line {self.line}: unterminated string")

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def add_number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == ".":
            if not self.peek_next().isdigit():
                raise ValueError(f"Line {self.line}: expected digit after '.'")
            self.advance()
            while self.peek().isdigit():
                self.advance()
            self.add_token(
                TokenType.NUMBER, float(self.source[self.start : self.current])
            )
        else:
            self.add_token(
                TokenType.NUMBER, int(self.source[self.start : self.current])
            )

    def add_keyword(self) -> None:
        while self.peek().isalpha():
            self.advance()

        keyword = self.source[self.start : self.current]
        match keyword:
            case "true":
                self.add_token(TokenType.BOOLEAN, True)
            case "false":
                self.add_token(TokenType.BOOLEAN, False)
            case "null":
                self.add_token(TokenType.NULL, None)
            case _:
                raise ValueError(f"Line {self.line}: unexpected keyword {keyword!r}")
