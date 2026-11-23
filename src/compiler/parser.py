from typing import List
from .tokens import Token, TokenType
from .ast_nodes import Expr, NumberLiteral, BinaryOp, UnaryOp, Variable, Assignment


class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"Parser error at line {token.line}, col {token.column}: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def _advance(self) -> Token:
        tok = self._peek()
        self.pos += 1
        return tok

    def _match(self, *expected_types: TokenType) -> bool:
        if self._peek().type in expected_types:
            self._advance()
            return True
        return False

    def _consume(self, expected_type: TokenType, error_msg: str) -> Token:
        if self._peek().type == expected_type:
            return self._advance()
        raise ParserError(f"{error_msg}, got {self._peek().type.name}", self._peek())

    def parse(self) -> Expr:
        expr = self._parse_assignment()
        if self._peek().type != TokenType.EOF:
            raise ParserError(f"Unexpected token '{self._peek().value}' after expression", self._peek())
        return expr

    def _parse_assignment(self) -> Expr:
        current = self._peek()
        if current.type == TokenType.IDENTIFIER:
            # Look ahead for '='
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                name_tok = self._advance()
                self._advance()  # consume '='
                val = self._parse_assignment()
                return Assignment(name=name_tok.value, value=val)

        return self._parse_addition()

    def _parse_addition(self) -> Expr:
        expr = self._parse_multiplication()
        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplication()
            expr = BinaryOp(left=expr, operator=op, right=right)
        return expr

    def _parse_multiplication(self) -> Expr:
        expr = self._parse_exponentiation()
        while self._peek().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._advance().value
            right = self._parse_exponentiation()
            expr = BinaryOp(left=expr, operator=op, right=right)
        return expr

    def _parse_exponentiation(self) -> Expr:
        expr = self._parse_unary()
        if self._match(TokenType.CARET):
            # Right-associative: 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2)
            right = self._parse_exponentiation()
            expr = BinaryOp(left=expr, operator="^", right=right)
        return expr

    def _parse_unary(self) -> Expr:
        if self._match(TokenType.MINUS):
            operand = self._parse_unary()
            return UnaryOp(operator="-", operand=operand)
        if self._match(TokenType.PLUS):
            return self._parse_unary()
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        tok = self._peek()

        if tok.type == TokenType.NUMBER:
            self._advance()
            val = float(tok.value)
            return NumberLiteral(value=val)

        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return Variable(name=tok.value)

        if self._match(TokenType.LPAREN):
            expr = self._parse_assignment()
            self._consume(TokenType.RPAREN, "Expected ')' after parenthesized expression")
            return expr

        raise ParserError(f"Unexpected token '{tok.value or tok.type.name}'", tok)
