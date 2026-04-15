import os
import subprocess
from typing import Dict, List, Any
from gitignore_manager import _is_ignored  # centralized — removes duplication

def get_file_status_map(root_path: str) -> Dict[str, str]:
    """Return dict of relative path -> tag ('clean', 'modified', 'untracked') for Git coloring."""
    status_map: Dict[str, str] = {}
    if not os.path.exists(os.path.join(root_path, ".git")):
        return status_map  # not a git repo → everything clean

    try:
        output = subprocess.check_output(
            ["git", "-C", root_path, "status", "--porcelain", "-uall"],
            text=True,
            stderr=subprocess.STDOUT
        ).strip()
        for line in output.splitlines():
            if not line:
                continue
            code = line[:2].strip()
            rel_path = line[3:].strip()
            if code.startswith("?"):
                status_map[rel_path] = "untracked"
            else:
                status_map[rel_path] = "modified"
    except Exception:
        pass  # graceful fallback
    return status_map


def build_interactive_structure(root_path: str) -> List[Dict[str, Any]]:
    """Build a complete list of rows for the two-column interactive Project Structure view.

    Each row dict contains everything the GUI needs:
      - type: 'dir', 'file', 'info', or 'error'
      - indent: str (tree prefix)
      - display_name: str (icon + name)
      - rel_path: str (for .gitignore operations)
      - tag: str (clean/modified/untracked for Git status coloring)
      - fg_color: str (text color)
      - is_ignored: bool
      - button_text: str ("❌" or "♻️")
      - button_fg: str (button color)
    """
    rows: List[Dict[str, Any]] = []
    status_map = get_file_status_map(root_path)

    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Skip .git directory entirely
            if ".git" in dirnames:
                dirnames.remove(".git")

            level = dirpath.replace(root_path, "").count(os.sep)
            indent = "│   " * level

            # Directory row
            rel_dir = os.path.relpath(dirpath, root_path)
            if rel_dir == ".":
                rel_dir = "."
            is_ignored_dir = _is_ignored(rel_dir, root_path)
            rows.append({
                "type": "dir",
                "indent": indent,
                "display_name": f"📁 {rel_dir}/",
                "rel_path": rel_dir,
                "tag": "clean",
                "fg_color": "#9ca3af" if is_ignored_dir else "#a5b4fc",
                "is_ignored": is_ignored_dir,
                "button_text": "♻️" if is_ignored_dir else "❌",
                "button_fg": "#eab308" if is_ignored_dir else "#ef4444"
            })

            # File rows
            file_indent = "│   " * (level + 1)
            for f in sorted(filenames):
                rel_file = os.path.join(rel_dir, f) if rel_dir != "." else f
                tag = status_map.get(rel_file, "clean")
                is_ignored = _is_ignored(rel_file, root_path)
                fg_color = "#9ca3af" if is_ignored else ("#f87171" if tag == "untracked" else "#facc15" if tag == "modified" else "#a5b4fc")
                rows.append({
                    "type": "file",
                    "indent": file_indent,
                    "display_name": f"📄 {f}",
                    "rel_path": rel_file,
                    "tag": tag,
                    "fg_color": fg_color,
                    "is_ignored": is_ignored,
                    "button_text": "♻️" if is_ignored else "❌",
                    "button_fg": "#eab308" if is_ignored else "#ef4444"
                })

            # Prevent huge trees from freezing UI
            if level > 6:
                rows.append({
                    "type": "info",
                    "indent": "   ",
                    "display_name": "... (deeper levels truncated for performance)",
                    "rel_path": "",
                    "tag": "clean",
                    "fg_color": "#a5b4fc",
                    "is_ignored": False,
                    "button_text": "",
                    "button_fg": ""
                })
                break

    except Exception as e:
        rows.append({
            "type": "error",
            "indent": "",
            "display_name": f"❌ Could not read structure: {e}",
            "rel_path": "",
            "tag": "untracked",
            "fg_color": "#ef4444",
            "is_ignored": False,
            "button_text": "",
            "button_fg": ""
        })

    return rows
