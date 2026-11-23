import pytest
from compiler.lexer import Lexer, LexerError
from compiler.tokens import TokenType


def test_tokenize_numbers_and_operators():
    tokens = Lexer("12.5 + 4 * (3 - 1)").tokenize()
    types = [t.type for t in tokens]
    assert types == [
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.STAR,
        TokenType.LPAREN,
        TokenType.NUMBER,
        TokenType.MINUS,
        TokenType.NUMBER,
        TokenType.RPAREN,
        TokenType.EOF,
    ]
    assert tokens[0].value == "12.5"
    assert tokens[2].value == "4"


def test_tokenize_variables_and_assignment():
    tokens = Lexer("x = 42 % 5 ^ 2").tokenize()
    types = [t.type for t in tokens]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.NUMBER,
        TokenType.PERCENT,
        TokenType.NUMBER,
        TokenType.CARET,
        TokenType.NUMBER,
        TokenType.EOF,
    ]


def test_lexer_error_on_invalid_char():
    with pytest.raises(LexerError) as exc_info:
        Lexer("10 + @ 5").tokenize()
    assert "Unexpected character '@'" in str(exc_info.value)
