from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any


class ASTVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: "NumberLiteral") -> Any:
        pass

    @abstractmethod
    def visit_binary(self, node: "BinaryOp") -> Any:
        pass

    @abstractmethod
    def visit_unary(self, node: "UnaryOp") -> Any:
        pass

    @abstractmethod
    def visit_variable(self, node: "Variable") -> Any:
        pass

    @abstractmethod
    def visit_assign(self, node: "Assignment") -> Any:
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> Any:
        pass


@dataclass(frozen=True)
class NumberLiteral(Expr):
    value: float

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_number(self)


@dataclass(frozen=True)
class Variable(Expr):
    name: str

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_variable(self)


@dataclass(frozen=True)
class UnaryOp(Expr):
    operator: str
    operand: Expr

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_unary(self)


@dataclass(frozen=True)
class BinaryOp(Expr):
    left: Expr
    operator: str
    right: Expr

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_binary(self)


@dataclass(frozen=True)
class Assignment(Expr):
    name: str
    value: Expr

    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_assign(self)
