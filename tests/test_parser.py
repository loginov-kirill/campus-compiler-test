import pytest
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserError
from compiler.ast_nodes import NumberLiteral, BinaryOp, UnaryOp, Variable, Assignment


def test_parse_precedence():
    tokens = Lexer("2 + 3 * 4").tokenize()
    ast = Parser(tokens).parse()
    # Should be 2 + (3 * 4)
    assert isinstance(ast, BinaryOp)
    assert ast.operator == "+"
    assert isinstance(ast.left, NumberLiteral) and ast.left.value == 2.0
    assert isinstance(ast.right, BinaryOp) and ast.right.operator == "*"


def test_parse_exponentiation_right_associativity():
    tokens = Lexer("2 ^ 3 ^ 2").tokenize()
    ast = Parser(tokens).parse()
    # 2 ^ (3 ^ 2)
    assert isinstance(ast, BinaryOp)
    assert ast.operator == "^"
    assert isinstance(ast.left, NumberLiteral) and ast.left.value == 2.0
    assert isinstance(ast.right, BinaryOp)
    assert ast.right.left.value == 3.0
    assert ast.right.right.value == 2.0


def test_parse_unary_minus():
    tokens = Lexer("-5 + 10").tokenize()
    ast = Parser(tokens).parse()
    assert isinstance(ast, BinaryOp)
    assert isinstance(ast.left, UnaryOp)
    assert ast.left.operator == "-"
    assert ast.left.operand.value == 5.0


def test_parse_assignment():
    tokens = Lexer("total = 100 * 1.2").tokenize()
    ast = Parser(tokens).parse()
    assert isinstance(ast, Assignment)
    assert ast.name == "total"
    assert isinstance(ast.value, BinaryOp)


def test_parser_unclosed_paren_error():
    tokens = Lexer("(10 + 5").tokenize()
    with pytest.raises(ParserError):
        Parser(tokens).parse()
