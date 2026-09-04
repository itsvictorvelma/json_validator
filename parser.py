import argparse
import sys
from pathlib import Path

from scanner import Scanner, Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> None:
        self.parse_value()
        self.consume(TokenType.EOF, "Expected end of input after JSON value")

    def parse_value(self) -> None:
        if self.check(TokenType.LEFT_BRACE):
            self.parse_object()
        elif self.check(TokenType.LEFT_BRACKET):
            self.parse_array()
        elif self.match(
            TokenType.STRING, TokenType.NUMBER, TokenType.BOOLEAN, TokenType.NULL
        ):
            return
        else:
            token = self.peek()
            raise ValueError(
                f"Line {token.line}: expected a JSON value, got {token.token_type}"
            )

    def parse_object(self) -> None:
        self.consume(TokenType.LEFT_BRACE, "Expected '{' at start of object")

        if self.check(TokenType.RIGHT_BRACE):
            self.advance()
            return

        self.parse_member()
        while self.match(TokenType.COMMA):
            self.parse_member()

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' at end of object")

    def parse_member(self) -> None:
        self.consume(TokenType.STRING, "Expected string key in object")
        self.consume(TokenType.COLON, "Expected ':' after object key")
        self.parse_value()

    def parse_array(self) -> None:
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' at start of array")

        if self.check(TokenType.RIGHT_BRACKET):
            self.advance()
            return

        self.parse_value()
        while self.match(TokenType.COMMA):
            self.parse_value()

        self.consume(TokenType.RIGHT_BRACKET, "Expected ']' at end of array")

    def peek(self) -> Token:
        return self.tokens[self.current]

    def advance(self) -> Token:
        token = self.peek()
        if not self.is_at_end():
            self.current += 1
        return token

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def check(self, token_type: TokenType) -> bool:
        return self.peek().token_type == token_type

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        token = self.peek()
        raise ValueError(f"Line {token.line}: {message} (got {token.token_type})")


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        description="Validate JSON files with a hand-written lexer and parser"
    )
    arg_parser.add_argument(
        "-f",
        "--filepath",
        type=Path,
        required=True,
        help="Path to the JSON file to validate",
    )
    args = arg_parser.parse_args()

    try:
        content = args.filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: File '{args.filepath}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for '{args.filepath}'.")
        sys.exit(1)

    try:
        tokens = Scanner(content).scan()
        Parser(tokens).parse()
    except ValueError as exc:
        print(f"Error: '{args.filepath}' is not valid JSON. ({exc})")
        sys.exit(1)

    print(f"Success: '{args.filepath}' is valid JSON.")
    sys.exit(0)


if __name__ == "__main__":
    main()
