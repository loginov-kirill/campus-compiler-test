# PyCalcLang — AST Expression Compiler & Stack VM

A lightweight arithmetic expression compiler and stack-based virtual machine written in Python.

## Architecture

1. **Lexer (`src/compiler/lexer.py`)**: Tokenizes input strings into mathematical operators, numbers, and identifiers.
2. **Parser (`src/compiler/parser.py`)**: Recursive descent Pratt/precedence parser producing an Abstract Syntax Tree (AST).
3. **Code Generator (`src/compiler/code_gen.py`)**: Traverses the AST and emits stack-based bytecode instructions.
4. **Virtual Machine (`src/compiler/vm.py`)**: Executes bytecode instructions using an execution stack and variable environment.
5. **CLI (`src/compiler/cli.py`)**: Interactive and batch CLI for compiling expressions and inspecting bytecode.

## Testing

```bash
pytest tests/ -v
```
