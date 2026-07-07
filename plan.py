import json
import os

TODO_PATH = ".agent/todos.json"


def _load():
    os.makedirs(".agent", exist_ok=True)

    if not os.path.exists(TODO_PATH):
        return []

    with open(TODO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(todos):
    os.makedirs(".agent", exist_ok=True)

    with open(TODO_PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


def add_todos(items):
    todos = _load()

    for item in items:
        todos.append({
            "title": item.get("title"),
            "description": item.get("description"),
            "verification": item.get("verification"),
            "status": "pending"
        })

    _save(todos)

    return {"todos": todos}


def get_todos():
    return {"todos": _load()}


def mark_todo(index, status, evidence=""):
    todos = _load()

    if index < 0 or index >= len(todos):
        return {"error": "Invalid todo index."}

    todos[index]["status"] = status
    todos[index]["evidence"] = evidence

    _save(todos)

    return {"todos": todos}