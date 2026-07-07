import os

TARGET_ROOT = os.path.abspath("target_repo")


def _safe_path(path):
    full_path = os.path.abspath(os.path.join(TARGET_ROOT, path))

    if not full_path.startswith(TARGET_ROOT):
        raise ValueError("Path outside target_repo is not allowed.")

    return full_path


def list_files(path="."):
    folder = _safe_path(path)
    ignore = {"__pycache__", ".pytest_cache", ".git"}

    if not os.path.exists(folder):
        return {"error": "Path not found."}

    items = []
    for root, dirs, files in os.walk(folder):
        if ".git" in root:
            continue

        for file in files:
            rel = os.path.relpath(os.path.join(root, file), TARGET_ROOT)
            items.append(rel)

        if len(items) > 100:
            break

    return {"files": items[:100]}


def read_file(path, start_line=1, read_lines=80):
    file_path = _safe_path(path)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    start = max(start_line - 1, 0)
    end = min(start + read_lines, len(lines))

    content = []
    for i in range(start, end):
        content.append(f"{i + 1}: {lines[i].rstrip()}")

    return {
        "path": path,
        "content": "\n".join(content),
        "start_line": start_line,
        "has_more": end < len(lines)
    }


def write_file(path, content):
    file_path = _safe_path(path)

    print("\n⚠️ Approval required to write file:")
    print(path)
    choice = input("Write this file? (y/n): ").strip().lower()

    if choice != "y":
        return {"approved": False, "status": "write denied"}

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"approved": True, "status": "written", "path": path}


def edit_file(path, start_line, end_line, new_text):
    file_path = _safe_path(path)

    if not os.path.exists(file_path):
        return {"error": "File not found."}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    old_text = "".join(lines[start_line - 1:end_line])

    print("\n⚠️ Approval required to edit file:")
    print(path)
    print("\nOLD:")
    print(old_text)
    print("\nNEW:")
    print(new_text)

    choice = input("Apply this edit? (y/n): ").strip().lower()

    if choice != "y":
        return {"approved": False, "status": "edit denied"}

    new_lines = [line + "\n" for line in new_text.split("\n")]
    lines[start_line - 1:end_line] = new_lines

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return {
        "approved": True,
        "status": "edited",
        "path": path,
        "diff_preview": {
            "old": old_text,
            "new": new_text
        }
    }