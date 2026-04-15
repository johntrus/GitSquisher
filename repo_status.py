import os
import subprocess
from typing import Dict, List, Tuple, Any

def get_repo_status(project_path: str, project_name: str = "") -> Dict[str, Any]:
    """Gather structured repository status information for the given project path.

    Returns a dict with:
      - valid: bool
      - directory: str
      - project_name: str (auto-filled from basename if empty)
      - is_git_repo: bool
      - branch: str or None
      - is_clean: bool
      - status_lines: list of (text: str, tag: str) tuples for easy GUI display
    """
    result: Dict[str, Any] = {
        "valid": True,
        "directory": project_path,
        "project_name": project_name.strip(),
        "is_git_repo": False,
        "branch": None,
        "is_clean": True,
        "status_lines": [],
    }

    # Validate path
    if not os.path.exists(project_path):
        result["valid"] = False
        result["status_lines"].append((f"❌ Directory does not exist:\n{project_path}\n", "error"))
        return result

    # Auto-fill project name from folder basename if not provided
    if not result["project_name"]:
        result["project_name"] = os.path.basename(project_path)
    result["status_lines"].append((f"📁 Loaded directory:\n{project_path}\n\n", "info"))
    result["status_lines"].append((f"📛 Project name: {result['project_name']}\n\n", "info"))

    # Check for Git repository
    git_dir = os.path.join(project_path, ".git")
    if os.path.exists(git_dir):
        result["is_git_repo"] = True
        result["status_lines"].append(("✅ Git repository initialized.\n", "success"))

        try:
            # Current branch
            branch = subprocess.check_output(
                ["git", "-C", project_path, "branch", "--show-current"],
                text=True,
                stderr=subprocess.STDOUT,
            ).strip()
            if branch:
                result["branch"] = branch
                result["status_lines"].append((f"🌿 Current branch: {branch}\n", "info"))

            # Working tree status
            status_output = subprocess.check_output(
                ["git", "-C", project_path, "status", "--porcelain"],
                text=True,
                stderr=subprocess.STDOUT,
            ).strip()
            result["is_clean"] = len(status_output) == 0
            if result["is_clean"]:
                result["status_lines"].append(("🧼 Working tree is clean\n", "success"))
            else:
                result["status_lines"].append(("⚠️  Working tree has uncommitted changes\n", "warning"))

        except subprocess.CalledProcessError:
            result["status_lines"].append(("⚠️ Could not read detailed Git status.\n", "warning"))
    else:
        result["status_lines"].append(("⚠️ Not yet a Git repository.\n", "warning"))
        result["status_lines"].append(("Run 'git init' to initialize.\n", "info"))

    result["status_lines"].append(("\n✅ Ready for GitSquisher commands.", "success"))
    return result


def format_status_for_gui(status: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return only the list of (text, tag) lines for direct insertion into the GUI text widget."""
    return status.get("status_lines", [])
