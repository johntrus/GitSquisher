import os
import subprocess
from typing import Dict, List, Any

def get_file_status_map(root_path: str) -> Dict[str, str]:
    """Return dict of relative path -> tag name ('clean', 'modified', 'untracked') for coloring."""
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
    """Build a list of structured rows for the two-column interactive Project Structure view.

    Each row is a dict with:
      - type: 'dir' or 'file'
      - indent: str (tree prefix)
      - display_name: str (icon + name)
      - rel_path: str (for .gitignore)
      - tag: str (clean/modified/untracked)
      - fg_color: str (for text color)
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
            rows.append({
                "type": "dir",
                "indent": indent,
                "display_name": f"📁 {rel_dir}/",
                "rel_path": rel_dir,
                "tag": "clean",
                "fg_color": "#a5b4fc"
            })

            # File rows
            file_indent = "│   " * (level + 1)
            for f in sorted(filenames):
                rel_file = os.path.join(rel_dir, f) if rel_dir != "." else f
                tag = status_map.get(rel_file, "clean")
                fg_color = "#f87171" if tag == "untracked" else "#facc15" if tag == "modified" else "#a5b4fc"
                rows.append({
                    "type": "file",
                    "indent": file_indent,
                    "display_name": f"📄 {f}",
                    "rel_path": rel_file,
                    "tag": tag,
                    "fg_color": fg_color
                })

            # Prevent huge trees from freezing UI
            if level > 6:
                rows.append({
                    "type": "info",
                    "indent": "   ",
                    "display_name": "... (deeper levels truncated for performance)",
                    "rel_path": "",
                    "tag": "clean",
                    "fg_color": "#a5b4fc"
                })
                break

    except Exception as e:
        rows.append({
            "type": "error",
            "indent": "",
            "display_name": f"❌ Could not read structure: {e}",
            "rel_path": "",
            "tag": "untracked",
            "fg_color": "#ef4444"
        })

    return rows
