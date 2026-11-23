import pytest
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.code_gen import BytecodeCompiler, OpCode
from compiler.vm import VirtualMachine, VMError


def eval_expr(expr_str: str, initial_env=None) -> float:
    tokens = Lexer(expr_str).tokenize()
    ast = Parser(tokens).parse()
    program = BytecodeCompiler().compile(ast)
    vm = VirtualMachine(initial_env)
    return vm.run(program)


def test_eval_basic_arithmetic():
    assert eval_expr("1 + 2 * 3") == 7.0
    assert eval_expr("(1 + 2) * 3") == 9.0
    assert eval_expr("10 - 4 - 2") == 4.0
    assert eval_expr("20 / 4 / 2") == 2.5
    assert eval_expr("10 % 3") == 1.0
    assert eval_expr("2 ^ 3 ^ 2") == 512.0  # 2 ^ 9


def test_eval_unary_and_variables():
    assert eval_expr("-5 + 15") == 10.0
    assert eval_expr("a * 2 + b", {"a": 4, "b": 3}) == 11.0


def test_eval_assignment():
    vm = VirtualMachine()
    tokens = Lexer("x = 5 + 3").tokenize()
    ast = Parser(tokens).parse()
    program = BytecodeCompiler().compile(ast)
    res = vm.run(program)
    assert res == 8.0
    assert vm.env["x"] == 8.0


def test_vm_division_by_zero():
    with pytest.raises(VMError) as exc_info:
        eval_expr("10 / 0")
    assert "Division by zero" in str(exc_info.value)


def test_vm_undefined_variable():
    with pytest.raises(VMError) as exc_info:
        eval_expr("foo + 1")
    assert "Undefined variable: 'foo'" in str(exc_info.value)
