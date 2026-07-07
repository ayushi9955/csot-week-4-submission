import os
import shlex
import subprocess

TARGET_ROOT = os.path.abspath("target_repo")

READ_ONLY_PREFIXES = [
    "dir", "ls", "type", "cat", "find", "grep", "git status",
    "git log", "git diff", "python -m pytest", "pytest"
]

DESTRUCTIVE_WORDS = [
    "rm", "del", "rmdir", "move", "mv", "copy", "cp",
    "git reset", "git clean", "pip install", "npm install",
    "write", "echo", ">", "sed -i"
]


def _ensure_target():
    os.makedirs(TARGET_ROOT, exist_ok=True)


def _is_read_only(command):
    command = command.strip().lower()
    return any(command.startswith(prefix) for prefix in READ_ONLY_PREFIXES)


def _is_destructive(command):
    command = command.strip().lower()
    return any(word in command for word in DESTRUCTIVE_WORDS)


def run_command(command, timeout=20):
    _ensure_target()

    risky = _is_destructive(command) or not _is_read_only(command)

    if risky:
        print("\n⚠️ Approval required before running:")
        print(command)
        choice = input("Run this command? (y/n): ").strip().lower()

        if choice != "y":
            return {
                "approved": False,
                "command": command,
                "stdout": "",
                "stderr": "User denied command.",
                "exit_code": None
            }

    try:
        result = subprocess.run(
            command,
            cwd=TARGET_ROOT,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "approved": True,
            "command": command,
            "stdout": result.stdout[-6000:],
            "stderr": result.stderr[-6000:],
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "approved": True,
            "command": command,
            "stdout": "",
            "stderr": "Command timed out.",
            "exit_code": -1
        }