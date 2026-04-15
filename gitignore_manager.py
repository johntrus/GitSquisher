import os
from typing import Tuple

def _is_ignored(rel_path: str, root_path: str) -> bool:
    """Check if the relative path appears in .gitignore (exact line match, ignoring comments/empty lines)."""
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
    """Append the selected item to .gitignore and return (success, message)."""
    gitignore_path = os.path.join(root_path, ".gitignore")
    try:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write(f"\n{rel_path}\n")
        return True, f"✅ Added '{rel_path}' to .gitignore"
    except Exception as e:
        return False, f"❌ Failed to add '{rel_path}' to .gitignore: {e}"


def remove_from_gitignore(rel_path: str, root_path: str) -> Tuple[bool, str]:
    """Remove the selected item from .gitignore (exact line match) and return (success, message)."""
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
