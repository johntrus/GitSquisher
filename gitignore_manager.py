import os
from typing import Tuple

def _is_ignored(rel_path: str, root_path: str) -> bool:
    """Check if a relative path is explicitly listed in .gitignore.

    Centralized single source of truth — used by git_structure.py and anywhere else
    that needs ignore status. Exact line match, ignores comments/blank lines.
    """
    gitignore_path = os.path.join(root_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        return False
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
        return rel_path in lines
    except Exception:
        return False


def add_to_gitignore(rel_path: str, root_path: str) -> Tuple[bool, str]:
    """Append the selected path to .gitignore (idempotent).

    Returns (success, user-friendly message) for immediate GUI feedback.
    """
    gitignore_path = os.path.join(root_path, ".gitignore")
    try:
        # Ensure file exists first
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("# GitSquisher-managed .gitignore\n\n")

        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write(f"{rel_path}\n")
        return True, f"✅ Added '{rel_path}' to .gitignore"
    except Exception as e:
        return False, f"❌ Failed to add '{rel_path}' to .gitignore: {e}"


def remove_from_gitignore(rel_path: str, root_path: str) -> Tuple[bool, str]:
    """Remove the exact line for rel_path from .gitignore (safe & clean).

    Returns (success, user-friendly message) for instant UI refresh.
    """
    gitignore_path = os.path.join(root_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        return False, f"❌ .gitignore does not exist for '{rel_path}'"

    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(gitignore_path, "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip() != rel_path:
                    f.write(line)

        return True, f"♻️ Removed '{rel_path}' from .gitignore"
    except Exception as e:
        return False, f"❌ Failed to remove '{rel_path}' from .gitignore: {e}"
