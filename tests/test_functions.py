import pytest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.code_gen import BytecodeCompiler
from compiler.vm import VirtualMachine, VMError


def eval_expr(expr_str: str) -> float:
    tokens = Lexer(expr_str).tokenize()
    ast = Parser(tokens).parse()
    program = BytecodeCompiler().compile(ast)
    vm = VirtualMachine()
    return vm.run(program)


def test_builtin_math_functions():
    assert eval_expr("sqrt(16)") == 4.0
    assert eval_expr("abs(-42)") == 42.0
    assert eval_expr("round(3.7)") == 4.0
    assert eval_expr("min(10, 5)") == 5.0
    assert eval_expr("max(10, 20)") == 20.0


def test_nested_function_calls():
    assert eval_expr("sqrt(max(9, 16))") == 4.0
    assert eval_expr("min(sqrt(100), abs(-7))") == 7.0


def test_function_in_arithmetic_expressions():
    assert eval_expr("2 * sqrt(25) + 3") == 13.0
    assert eval_expr("max(4 * 2, 3 + 4)") == 8.0


def test_unknown_function_error():
    with pytest.raises(VMError) as exc:
        eval_expr("unknown_fn(1, 2)")
    assert "Unknown function: 'unknown_fn'" in str(exc.value)


def test_wrong_argument_count():
    with pytest.raises(VMError) as exc:
        eval_expr("sqrt(4, 9)")
    assert "expects 1 argument" in str(exc.value)
