import os
from datetime import datetime
from typing import Tuple

def apply_ignore_template(project_path: str, project_name: str = "") -> Tuple[bool, str]:
    """Apply the standardized GitSquisher .gitignore template while safely preserving any user custom entries.

    This function is kept for backward compatibility and one-click template resets.
    It no longer overlaps with the live .gitignore_manager.py logic — it only rewrites the file when explicitly called.
    """
    gitignore_path = os.path.join(project_path, ".gitignore")
    today = datetime.now().strftime("%m-%d-%Y")
    project_name = project_name or os.path.basename(project_path)

    # === EVEN MORE ROBUST TEMPLATE ===
    template = f"""# ================================================
# '{project_name}' - ROBUST .GITIGNORE ({today})
# ================================================
# GitSquisher enhanced template for Python + Tkinter + AI/ML + GUI projects

# Git internals
.git/

# Virtual environments
venv/
.venv/
env/
ENV/
env.bak/
venv.bak/

# Python packaging & build
*.egg-info/
dist/
build/
wheels/
*.whl
MANIFEST

# Python bytecode & caches
__pycache__/
*.pyc
*.pyo
*.pyd
*.cpython-*.pyc
*.so

# Testing & coverage
.pytest_cache/
.coverage
coverage.xml
htmlcov/
.tox/
.nox/
.mypy_cache/
.ruff_cache/

# Jupyter
.ipynb_checkpoints/

# Security & encryption (GitSquisher specific)
*.key
*.enc
*.pem
secrets.json
credentials.json
.env
.env.local
.env.*
!.env.example
grem_encryption.key

# AI/ML artifacts
models/
wandb/
mlruns/
tensorboard/
lightning_logs/
*.safetensors
*.bin
*.pt
*.pth
*.gguf

# Logs and temp files
*.log
logs/
*.tmp
*.backup
*~

# Editor & OS files
.DS_Store
Thumbs.db
.vscode/
.idea/
*.swp
*.swo

# Docker
.docker/
.dockerignore

# Squished archives (auto-managed by GitSquisher)
squishes/

# ================================================
# USER CUSTOM ENTRIES (preserved from previous .gitignore)
# ================================================
"""

    # Preserve any existing custom entries
    custom_lines: list[str] = []
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#"):
                        custom_lines.append(line.rstrip())
        except Exception as e:
            return False, f"❌ Failed to read existing .gitignore: {e}"

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
        return True, f"✅ Applied robust GitSquisher .gitignore template for '{project_name}' (custom entries preserved)"
    except Exception as e:
        return False, f"❌ Failed to write .gitignore template: {e}"


def clear_ignore_list(project_path: str) -> Tuple[bool, str]:
    """Completely reset .gitignore to a minimal state (ready for a fresh template).

    Used only when the user explicitly wants a clean slate.
    """
    gitignore_path = os.path.join(project_path, ".gitignore")
    try:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("# .gitignore reset by GitSquisher — ready for new template\n")
        return True, "✅ .gitignore has been reset to empty (ready for new template)"
    except Exception as e:
        return False, f"❌ Failed to clear .gitignore: {e}"
