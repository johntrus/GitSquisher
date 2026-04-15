import os
from cryptography.fernet import Fernet
from datetime import datetime
from squisher import create_squish, list_squishable_files

def _get_key_path(project_path: str) -> str:
    """Return the path to the encryption key (already ignored by .gitignore)."""
    return os.path.join(project_path, "grem_encryption.key")


def generate_encryption_key(project_path: str) -> tuple[bool, str]:
    """Generate a new Fernet key (AES-256) and save it as grem_encryption.key if it doesn't exist.

    Returns (success, message). Key is never committed because .gitignore already excludes it.
    """
    key_path = _get_key_path(project_path)
    if os.path.exists(key_path):
        return True, "✅ Encryption key already exists (re-using secure key)"

    try:
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
        return True, f"✅ New encryption key generated and saved to grem_encryption.key"
    except Exception as e:
        return False, f"❌ Failed to generate encryption key: {str(e)}"


def encrypt_squish(project_path: str, project_name: str) -> tuple[bool, str]:
    """Create a fresh squish then encrypt it with the repo's Fernet key.

    The encrypted .enc file is placed inside squishes/ alongside the original zip.
    Returns (success, message) with full path to the encrypted archive.
    """
    # First ensure we have a key
    success, msg = generate_encryption_key(project_path)
    if not success:
        return False, msg

    # Create the clean squish first (re-uses all existing logic)
    squish_success, squish_msg = create_squish(project_path, project_name)
    if not squish_success:
        return False, f"❌ Squish failed before encryption: {squish_msg}"

    # Locate the newest zip in squishes/
    squishes_dir = os.path.join(project_path, "squishes")
    zip_files = [f for f in os.listdir(squishes_dir) if f.endswith(".zip")]
    if not zip_files:
        return False, "❌ No squish zip found to encrypt"

    latest_zip = max(
        [os.path.join(squishes_dir, f) for f in zip_files],
        key=os.path.getmtime
    )
    zip_filename = os.path.basename(latest_zip)

    # Encrypt the zip
    enc_filename = zip_filename.replace(".zip", ".enc")
    enc_path = os.path.join(squishes_dir, enc_filename)

    try:
        with open(_get_key_path(project_path), "rb") as f:
            key = f.read()
        fernet = Fernet(key)

        with open(latest_zip, "rb") as f:
            data = f.read()

        encrypted = fernet.encrypt(data)

        with open(enc_path, "wb") as f:
            f.write(encrypted)

        return True, f"✅ Encrypted {zip_filename} → {enc_filename} (secure AES-256)"
    except Exception as e:
        return False, f"❌ Encryption failed: {str(e)}"


def decrypt_file(enc_path: str, project_path: str, output_path: str = None) -> tuple[bool, str]:
    """Decrypt an .enc file back to original using the repo's key (utility for completeness)."""
    if not os.path.exists(enc_path):
        return False, "❌ Encrypted file not found"

    try:
        with open(_get_key_path(project_path), "rb") as f:
            key = f.read()
        fernet = Fernet(key)

        with open(enc_path, "rb") as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted)

        if output_path is None:
            output_path = enc_path.replace(".enc", "_decrypted.zip")

        with open(output_path, "wb") as f:
            f.write(decrypted)

        return True, f"✅ Decrypted to {os.path.basename(output_path)}"
    except Exception as e:
        return False, f"❌ Decryption failed (wrong key?): {str(e)}"
