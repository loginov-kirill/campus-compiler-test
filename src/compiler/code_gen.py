from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Any
from .ast_nodes import ASTVisitor, Expr, NumberLiteral, BinaryOp, UnaryOp, Variable, Assignment


class OpCode(Enum):
    PUSH_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    NEG = auto()
    HALT = auto()


@dataclass(frozen=True)
class Instruction:
    op: OpCode
    arg: Any = None

    def __repr__(self) -> str:
        if self.arg is not None:
            return f"{self.op.name} {self.arg}"
        return self.op.name


class BytecodeCompiler(ASTVisitor):
    def __init__(self):
        self.instructions: List[Instruction] = []

    def compile(self, ast: Expr) -> List[Instruction]:
        self.instructions = []
        ast.accept(self)
        self.instructions.append(Instruction(OpCode.HALT))
        return list(self.instructions)

    def visit_number(self, node: NumberLiteral) -> None:
        self.instructions.append(Instruction(OpCode.PUSH_CONST, node.value))

    def visit_variable(self, node: Variable) -> None:
        self.instructions.append(Instruction(OpCode.LOAD_VAR, node.name))

    def visit_unary(self, node: UnaryOp) -> None:
        node.operand.accept(self)
        if node.operator == "-":
            self.instructions.append(Instruction(OpCode.NEG))
        else:
            raise ValueError(f"Unknown unary operator: {node.operator}")

    def visit_binary(self, node: BinaryOp) -> None:
        node.left.accept(self)
        node.right.accept(self)
        if node.operator == "+":
            self.instructions.append(Instruction(OpCode.ADD))
        elif node.operator == "-":
            self.instructions.append(Instruction(OpCode.SUB))
        elif node.operator == "*":
            self.instructions.append(Instruction(OpCode.MUL))
        elif node.operator == "/":
            self.instructions.append(Instruction(OpCode.DIV))
        elif node.operator == "%":
            self.instructions.append(Instruction(OpCode.MOD))
        elif node.operator == "^":
            self.instructions.append(Instruction(OpCode.POW))
        else:
            raise ValueError(f"Unknown binary operator: {node.operator}")

    def visit_assign(self, node: Assignment) -> None:
        node.value.accept(self)
        self.instructions.append(Instruction(OpCode.STORE_VAR, node.name))
