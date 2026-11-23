import subprocess
import sys


def test_cli_execution():
    cmd = [sys.executable, "-m", "compiler.cli", "2 + 3 * 4", "--disasm"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd="src")
    assert proc.returncode == 0
    assert "=== Bytecode Disassembly ===" in proc.stdout
    assert "PUSH_CONST 2.0" in proc.stdout
    assert "PUSH_CONST 3.0" in proc.stdout
    assert "MUL" in proc.stdout
    assert "ADD" in proc.stdout
    assert "14.0" in proc.stdout
