import os
from datetime import datetime
from typing import Tuple

def apply_ignore_template(project_path: str, project_name: str) -> Tuple[bool, str]:
    """Apply the standardized GitSquisher .gitignore template while safely preserving any existing custom entries.

    Reads the current .gitignore (if present), keeps all user-defined patterns,
    then rewrites with a clean dated header + standard sections + preserved customs.
    Returns (True, success_message) or (False, error_message).
    """
    gitignore_path = os.path.join(project_path, ".gitignore")
    today = datetime.now().strftime("%m-%d-%Y")

    # Modern, general-purpose GitSquisher template (suitable for any Python + AI/ML project)
    template = f"""# ================================================
# '{project_name}' - COMPLETE .GITIGNORE ({today})
# ================================================
# GitSquisher standard template for Python + AI/ML projects
# (prevents large model files, caches, and temp data from bloating repos)

# Git internals
.git/

# Python bytecode & caches
__pycache__/
*.pyc
*.pyo
*.pyd
*.cpython-*.pyc

# Security & encryption files
*.key
*.enc
*.pem
secrets.json
credentials.json
.env
.env.local

# Large model / tokenizer / AI artifacts (common in ML projects)
models/
tokenizer.json
vocab.json
merges.txt
*.safetensors
*.bin
*.pt
*.pth
*.gguf
*.ckpt
*.h5
*.onnx
*.pb
model.safetensors.index.json

# Runtime / temporary JSON files
load_model.json
load_bar.json
progress_*.json
*.jsonl

# Backups and editor junk
*.backup
*.tmp
*~
.DS_Store
Thumbs.db
.vscode/
.idea/
*.swp
*.swo

# Logs and build artifacts
*.log
dist/
build/
*.egg-info/
__pycache__/

# Optional: any future large folders
# (add your own custom patterns below)
"""

    # Preserve existing custom user entries
    custom_lines: list[str] = []
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#"):
                        custom_lines.append(line.rstrip())
        except Exception as e:
            return False, f"Failed to read existing .gitignore: {e}"

    # Combine template + preserved customs
    full_content = template
    if custom_lines:
        full_content += "\n# ================================================\n"
        full_content += "# USER CUSTOM ENTRIES (preserved from previous .gitignore)\n"
        full_content += "# ================================================\n"
        full_content += "\n".join(custom_lines) + "\n"

    try:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        return True, f"✅ Applied full GitSquisher template for '{project_name}' (custom entries preserved)"
    except Exception as e:
        return False, f"❌ Failed to write .gitignore template: {e}"


def clear_ignore_list(project_path: str) -> Tuple[bool, str]:
    """Completely reset .gitignore to a minimal default/empty state after confirmation.

    Creates (or truncates) .gitignore with only a reset comment.
    Returns (True, success_message) or (False, error_message).
    """
    gitignore_path = os.path.join(project_path, ".gitignore")
    try:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("# .gitignore reset by GitSquisher - ready for new template\n")
        return True, "✅ .gitignore has been reset to empty (ready for new template)"
    except Exception as e:
        return False, f"❌ Failed to clear .gitignore: {e}"
