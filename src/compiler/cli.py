import argparse
import sys
from .lexer import Lexer
from .parser import Parser
from .code_gen import BytecodeCompiler
from .vm import VirtualMachine


def compile_and_eval(expression: str) -> (float, str):
    tokens = Lexer(expression).tokenize()
    ast = Parser(tokens).parse()
    compiler = BytecodeCompiler()
    program = compiler.compile(ast)
    disasm = "\n".join(f"{i:04d}: {repr(inst)}" for i, inst in enumerate(program))
    vm = VirtualMachine()
    res = vm.run(program)
    return res, disasm


def main():
    parser = argparse.ArgumentParser(description="PyCalcLang AST Compiler & Bytecode VM")
    parser.add_argument("expr", nargs="?", help="Expression to compile and evaluate")
    parser.add_argument("--disasm", action="store_true", help="Print compiled bytecode disassembly")
    args = parser.parse_args()

    if not args.expr:
        print("Usage: python -m compiler.cli <expression> [--disasm]")
        sys.exit(1)

    result, disasm = compile_and_eval(args.expr)
    if args.disasm:
        print("=== Bytecode Disassembly ===")
        print(disasm)
        print("=== Execution Result ===")
    print(result)


if __name__ == "__main__":
    main()
