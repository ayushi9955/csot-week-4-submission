import ast
import os

TARGET_ROOT = os.path.abspath("target_repo")


def _safe_path(path):
    full_path = os.path.abspath(os.path.join(TARGET_ROOT, path))

    if not full_path.startswith(TARGET_ROOT):
        raise ValueError("Path outside target_repo is not allowed.")

    return full_path


def grep(pattern, path="."):
    folder = _safe_path(path)
    matches = []

    for root, dirs, files in os.walk(folder):
        if ".git" in root:
            continue

        for file in files:
            if not file.endswith((".py", ".md", ".txt", ".json", ".yml", ".yaml")):
                continue

            file_path = os.path.join(root, file)
            rel = os.path.relpath(file_path, TARGET_ROOT)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, start=1):
                        if pattern.lower() in line.lower():
                            matches.append({
                                "file": rel,
                                "line": line_no,
                                "text": line.strip()
                            })
            except Exception:
                pass

            if len(matches) >= 50:
                return {"matches": matches}

    return {"matches": matches}


def list_definitions(path):
    file_path = _safe_path(path)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"error": "Could not parse Python file."}

    defs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defs.append({
                "type": "function",
                "name": node.name,
                "line": node.lineno
            })

        elif isinstance(node, ast.ClassDef):
            defs.append({
                "type": "class",
                "name": node.name,
                "line": node.lineno
            })

    return {"definitions": defs}