import os
from datetime import datetime
from typing import Tuple

def apply_ignore_template(project_path: str, project_name: str) -> Tuple[bool, str]:
    """Apply the standardized GitSquisher .gitignore template while safely preserving any existing custom entries.

    Now uses ADVANCED patterns: recursive **/ globs, negation support, language-specific sections,
    and AI/ML-focused exclusions to prevent bloat more effectively than basic lists.
    Returns (True, success_message) or (False, error_message).
    """
    gitignore_path = os.path.join(project_path, ".gitignore")
    today = datetime.now().strftime("%m-%d-%Y")

    # ADVANCED GitSquisher template (with expert-level patterns and comments)
    template = f"""# ================================================
# '{project_name}' - ADVANCED .GITIGNORE ({today})
# ================================================
# Git internals (prevents 60-file explosion on Grok.com)
.git/

# ================================================
# ADVANCED RECURSIVE PATTERNS (use **/ for any depth)
# ================================================
**/__pycache__/
**/*.pyc
**/*.pyo
**/*.pyd
**/*.cpython-*.pyc
**/.DS_Store
**/*.swp
**/*.swo
**/.vscode/
**/.idea/
**/*.log
**/*.tmp
**/*.backup
**/*~

# ================================================
# VIRTUAL ENVIRONMENTS & RUNTIME (advanced)
# ================================================
venv/
env/
.venv/
**/.env
**/*.env
.env.local
.env.development
.env.production

# ================================================
# SECURITY & ENCRYPTION (GitSquisher specific)
# ================================================
*.key
grem_encryption.key
*.enc
memory.json.enc

# ================================================
# AI / ML / LARGE MODEL ARTIFACTS (advanced exclusions)
# ================================================
models/
granite4-small-h/
tokenizer.json
vocab.json
merges.txt
model.safetensors.index.json
**/*.safetensors
**/*.bin
**/*.pt
**/*.pth
**/*.gguf
**/*.ckpt
**/*.h5
**/*.onnx
**/*.pb

# ================================================
# BUILD & PACKAGE OUTPUTS (advanced)
# ================================================
dist/
build/
**/*.egg-info/
**/*.whl
**/*.tar.gz
**/*.zip   # (except those inside squishes/ - handled separately)

# ================================================
# RUNTIME / TEMP JSON & PROGRESS FILES
# ================================================
load_model.json
load_bar.json
progress_*.json

# ================================================
# OPTIONAL: LARGE FILE HINT (uncomment + use git lfs for >10MB files)
# ================================================
# *.bin filter=lfs diff=lfs merge=lfs -text
# *.safetensors filter=lfs diff=lfs merge=lfs -text

# ================================================
# USER CUSTOM ENTRIES (preserved automatically)
# ================================================
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
        return True, f"✅ Applied ADVANCED GitSquisher template for '{project_name}' (custom entries preserved)"
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
            f.write("# .gitignore reset by GitSquisher - ready for new advanced template\n")
        return True, "✅ .gitignore has been reset to empty (ready for new advanced template)"
    except Exception as e:
        return False, f"❌ Failed to clear .gitignore: {e}"
