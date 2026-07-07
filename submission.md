# Week 4 Submission – Code Scout

## Introduction

For Week 4, I built **Code Scout**, a command-line coding agent that can inspect an unfamiliar codebase, understand the task, create a plan, modify code safely, verify the fix, and report the results.

The project builds on the previous week's Research Desk agent by replacing web-based research with repository exploration and code editing. Instead of simply answering questions, the agent now performs multiple steps to solve programming tasks while keeping the user in control of any potentially destructive action.

---

# Project Structure

```
week4/
│
├── agent.py
├── AGENTS.md
├── requirements.txt
├── .env.example
├── tools/
│   ├── exec.py
│   ├── files.py
│   ├── search.py
│   └── plan.py
├── target_repo/
└── .agent/
```

---

# Features Implemented

The agent includes the following capabilities:

- Interactive REPL mode
- One-shot CLI mode
- Session persistence and resume
- Automatic title generation for sessions
- Tool calling through the language model
- Repository exploration
- Grep-based search
- Python definition search
- File reading with line numbers
- Safe file writing
- Safe file editing with approval
- Command execution inside `target_repo`
- Todo planning system
- Verification using test commands
- AGENTS.md loading
- Sandboxed file operations

---

# Agent Workflow

Whenever a task is given, the agent follows this workflow:

1. Understand the user's request.
2. Explore the repository using search tools.
3. Create a todo list describing the required steps.
4. Read only the necessary files.
5. Propose edits when required.
6. Ask for approval before changing files or executing risky commands.
7. Apply the approved changes.
8. Run verification commands such as `pytest`.
9. Mark the todo item complete only if verification succeeds.
10. Save the updated session and produce a final report.

---

# Tools

The following tools were implemented:

- run_command
- list_files
- read_file
- write_file
- edit_file
- grep
- list_definitions
- add_todos
- get_todos
- mark_todo

---

# Safety Features

To prevent accidental changes:

- Every destructive shell command requires user approval.
- File modifications display the proposed change before writing.
- All commands are executed only inside `target_repo`.
- The agent never claims success without running a verification command.

---

# Example Task

The agent was tested on a sample repository containing a failing calculator implementation.

The workflow was:

1. Run the test suite.
2. Observe the failing test.
3. Search for the affected function.
4. Read the implementation.
5. Replace the incorrect logic.
6. Re-run the tests.
7. Confirm exit code `0`.
8. Mark the task as completed.

This demonstrated the complete explore → plan → edit → verify workflow.

---

# Challenges Faced

One challenge was storing OpenAI tool-call messages in JSON sessions. Tool-call objects are not directly serializable, which caused session saving to fail. This was resolved by converting messages to dictionaries before writing them to disk.

Another challenge was designing safe file editing while still allowing the model to modify code. Adding an approval step before every write operation solved this problem.

---

# Setup Instructions

1. Create and activate a virtual environment.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file.

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=openrouter/free
```

4. Place the repository to investigate inside:

```
target_repo/
```

5. Start interactive mode.

```bash
python agent.py
```

6. Run a one-shot task.

```bash
python agent.py "Find and fix the failing test"
```

7. Resume an earlier session.

```bash
python agent.py --session demo
```

---

# Conclusion

This project extends the previous week's agent into an autonomous coding assistant capable of exploring repositories, planning multi-step tasks, safely modifying files, verifying changes through real commands, and maintaining persistent sessions. The design focuses on correctness, transparency, and safety while keeping the workflow modular and easy to extend.