import math
from typing import Dict, List, Any
from .code_gen import Instruction, OpCode


class VMError(Exception):
    pass


BUILTIN_FUNCS = {
    "sqrt": (math.sqrt, 1),
    "abs": (abs, 1),
    "sin": (math.sin, 1),
    "cos": (math.cos, 1),
    "tan": (math.tan, 1),
    "round": (round, 1),
    "log": (math.log, 1),
    "exp": (math.exp, 1),
    "min": (min, -1),
    "max": (max, -1),
}


class VirtualMachine:
    def __init__(self, initial_env: Dict[str, float] = None):
        self.stack: List[float] = []
        self.env: Dict[str, float] = dict(initial_env or {})

    def run(self, program: List[Instruction]) -> float:
        pc = 0
        while pc < len(program):
            inst = program[pc]
            pc += 1

            if inst.op == OpCode.HALT:
                break
            elif inst.op == OpCode.PUSH_CONST:
                self.stack.append(float(inst.arg))
            elif inst.op == OpCode.LOAD_VAR:
                name = str(inst.arg)
                if name not in self.env:
                    raise VMError(f"Undefined variable: '{name}'")
                self.stack.append(self.env[name])
            elif inst.op == OpCode.STORE_VAR:
                if not self.stack:
                    raise VMError("Stack underflow during STORE_VAR")
                val = self.stack[-1]
                self.env[str(inst.arg)] = val
            elif inst.op == OpCode.NEG:
                if not self.stack:
                    raise VMError("Stack underflow during NEG")
                self.stack.append(-self.stack.pop())
            elif inst.op == OpCode.ADD:
                b = self._pop_two()
                self.stack.append(b[0] + b[1])
            elif inst.op == OpCode.SUB:
                b = self._pop_two()
                self.stack.append(b[0] - b[1])
            elif inst.op == OpCode.MUL:
                b = self._pop_two()
                self.stack.append(b[0] * b[1])
            elif inst.op == OpCode.DIV:
                b = self._pop_two()
                if b[1] == 0:
                    raise VMError("Division by zero")
                self.stack.append(b[0] / b[1])
            elif inst.op == OpCode.MOD:
                b = self._pop_two()
                if b[1] == 0:
                    raise VMError("Modulo by zero")
                self.stack.append(b[0] % b[1])
            elif inst.op == OpCode.POW:
                b = self._pop_two()
                self.stack.append(b[0] ** b[1])
            elif inst.op == OpCode.CALL_FUNC:
                func_name, argc = inst.arg
                if func_name not in BUILTIN_FUNCS:
                    raise VMError(f"Unknown function: '{func_name}'")
                func, expected_argc = BUILTIN_FUNCS[func_name]
                if expected_argc > 0 and argc != expected_argc:
                    raise VMError(f"Function '{func_name}' expects {expected_argc} argument(s), got {argc}")
                if len(self.stack) < argc:
                    raise VMError("Stack underflow during CALL_FUNC")
                args = [self.stack.pop() for _ in range(argc)]
                args.reverse()
                try:
                    res = float(func(*args))
                except Exception as e:
                    raise VMError(f"Error in function '{func_name}': {e}")
                self.stack.append(res)
            else:
                raise VMError(f"Unknown opcode: {inst.op}")

        if not self.stack:
            return 0.0
        return self.stack[-1]

    def _pop_two(self) -> (float, float):
        if len(self.stack) < 2:
            raise VMError("Stack underflow")
        b = self.stack.pop()
        a = self.stack.pop()
        return (a, b)
