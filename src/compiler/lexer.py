from typing import List
from .tokens import Token, TokenType


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer error at line {line}, col {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ""

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < len(self.source):
            ch = self._peek()

            if ch.isspace():
                self._advance()
                continue

            start_col = self.column
            start_line = self.line

            if ch.isdigit() or ch == ".":
                num_str = ""
                has_dot = False
                while self._peek().isdigit() or (self._peek() == "." and not has_dot):
                    if self._peek() == ".":
                        has_dot = True
                    num_str += self._advance()
                tokens.append(Token(TokenType.NUMBER, num_str, start_line, start_col))
                continue

            if ch.isalpha() or ch == "_":
                ident_str = ""
                while self._peek().isalnum() or self._peek() == "_":
                    ident_str += self._advance()
                tokens.append(Token(TokenType.IDENTIFIER, ident_str, start_line, start_col))
                continue

            if ch == "+":
                self._advance()
                tokens.append(Token(TokenType.PLUS, "+", start_line, start_col))
            elif ch == "-":
                self._advance()
                tokens.append(Token(TokenType.MINUS, "-", start_line, start_col))
            elif ch == "*":
                self._advance()
                tokens.append(Token(TokenType.STAR, "*", start_line, start_col))
            elif ch == "/":
                self._advance()
                tokens.append(Token(TokenType.SLASH, "/", start_line, start_col))
            elif ch == "%":
                self._advance()
                tokens.append(Token(TokenType.PERCENT, "%", start_line, start_col))
            elif ch == "^":
                self._advance()
                tokens.append(Token(TokenType.CARET, "^", start_line, start_col))
            elif ch == "(":
                self._advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif ch == ")":
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif ch == "=":
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
            elif ch == ",":
                self._advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
            else:
                bad_char = self._advance()
                raise LexerError(f"Unexpected character '{bad_char}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
