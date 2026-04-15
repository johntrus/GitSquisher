import os
import zipfile
import subprocess
from datetime import datetime
from gitignore_manager import _is_ignored

def create_squish(project_path: str, project_name: str, include_untracked: bool = False) -> tuple[bool, str]:
    """Create a squished zip of the project, respecting .gitignore.

    Now stores ALL zips in a clean 'squishes/' subfolder (auto-created + auto-added to .gitignore)
    so the project root stays pristine.
    """
    if not os.path.exists(project_path):
        return False, "Project path does not exist."

    # Auto-create squishes/ subfolder
    squishes_dir = os.path.join(project_path, "squishes")
    os.makedirs(squishes_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{project_name}_squished_{timestamp}.zip"
    zip_path = os.path.join(squishes_dir, zip_filename)

    # Auto-add "squishes/" to .gitignore if not already present
    gitignore_path = os.path.join(project_path, ".gitignore")
    try:
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "squishes/" not in content:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write("\n# Squished archives (auto-added by GitSquisher)\nsquishes/\n")
    except:
        pass  # graceful fallback

    try:
        # Prefer git archive if it's a git repo (respects .gitignore perfectly)
        git_dir = os.path.join(project_path, ".git")
        if os.path.exists(git_dir):
            try:
                subprocess.check_call([
                    "git", "-C", project_path, "archive", "--format=zip",
                    "-o", zip_path, "HEAD"
                ])
                return True, f"✅ Successfully created {zip_filename} → squishes/ (git archive)"
            except subprocess.CalledProcessError:
                pass  # fallback to manual method

        # Manual fallback zipping
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                # Skip .git and the squishes folder itself
                if ".git" in dirs:
                    dirs.remove(".git")
                if "squishes" in dirs:
                    dirs.remove("squishes")

                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, project_path)

                    # Skip ignored files
                    if _is_ignored(rel_path, project_path):
                        continue

                    zipf.write(full_path, rel_path)

        return True, f"✅ Successfully created {zip_filename} → squishes/ (manual method)"

    except Exception as e:
        return False, f"❌ Failed to create squish: {str(e)}"


def list_squishable_files(project_path: str) -> list:
    """Return list of files that would be included in a squish (not ignored)."""
    files = []
    if not os.path.exists(project_path):
        return files
    try:
        for root, dirs, filenames in os.walk(project_path):
            if ".git" in dirs:
                dirs.remove(".git")
            if "squishes" in dirs:
                dirs.remove("squishes")
            for f in filenames:
                rel = os.path.relpath(os.path.join(root, f), project_path)
                if not _is_ignored(rel, project_path):
                    files.append(rel)
    except:
        pass
    return files
