import subprocess
import sys
import pytest

def test_implicit_add_integration():
    """
    Verifies that calling the module without 'add' subcommand treats args as task text.
    """
    # Assuming the package is installed or we can run via python -m
    cmd = [sys.executable, "-m", "tskcli.cli", "Implicit Task Test"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Task created" in result.stdout
    assert "Implicit Task Test" in result.stdout

def test_explicit_add_integration():
    cmd = [sys.executable, "-m", "tskcli.cli", "add", "Explicit Task Test"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Task created" in result.stdout
    assert "Explicit Task Test" in result.stdout
