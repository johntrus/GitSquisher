import os
import secrets
from typing import Tuple, Optional, List
from cryptography.fernet import Fernet, MultiFernet, InvalidToken
from datetime import datetime

# Automated rotation interval (cryptographic best practice)
ROTATION_INTERVAL_DAYS = 90


def _get_key_path(project_path: str) -> str:
    """Return the absolute path to grem_encryption.key (always ignored by .gitignore)."""
    return os.path.join(project_path, "grem_encryption.key")


def _load_all_keys(project_path: str) -> List[bytes]:
    """Internal helper: load every key from the key file (one key per line)."""
    key_path = _get_key_path(project_path)
    if not os.path.exists(key_path):
        return []
    with open(key_path, "rb") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def _save_all_keys(project_path: str, keys: List[bytes]) -> None:
    """Internal helper: write all keys back to file (newest first)."""
    key_path = _get_key_path(project_path)
    with open(key_path, "wb") as f:
        for k in keys:
            f.write(k + b"\n")
    os.chmod(key_path, 0o600)


def get_key_age_days(project_path: str) -> int:
    """Return the age of the key file in days (0 if missing)."""
    key_path = _get_key_path(project_path)
    if not os.path.exists(key_path):
        return 0
    mtime = os.path.getmtime(key_path)
    age = (datetime.now() - datetime.fromtimestamp(mtime)).days
    return age


def should_auto_rotate(project_path: str) -> bool:
    """Return True if the key is older than the rotation interval."""
    return get_key_age_days(project_path) > ROTATION_INTERVAL_DAYS


def auto_rotate_if_needed(project_path: str) -> Tuple[bool, str]:
    """Automatically rotate the key if it exceeds the age threshold.
    Called transparently before every encrypt operation.
    """
    if should_auto_rotate(project_path):
        return rotate_encryption_key(project_path)
    return True, "✅ Key is fresh — no rotation needed"


def generate_encryption_key(project_path: str) -> Tuple[bool, str]:
    """Generate the very first secure Fernet key (AES-256) if none exists.
    Never overwrites an existing key file.
    """
    key_path = _get_key_path(project_path)
    if os.path.exists(key_path):
        return True, "✅ Encryption key already exists (re-using secure key)"

    try:
        key = Fernet.generate_key()
        _save_all_keys(project_path, [key])
        return True, f"✅ New secure AES-256 key generated and saved to grem_encryption.key"
    except Exception as e:
        return False, f"❌ Failed to generate encryption key: {str(e)}"


def get_multifernet(project_path: str) -> Tuple[bool, Optional[MultiFernet], str]:
    """Return a MultiFernet ready for encryption (newest key first) and decryption (all keys)."""
    keys = _load_all_keys(project_path)
    if not keys:
        return False, None, "❌ No encryption key found. Please run Encrypt & Key first."

    try:
        fernet_list = [Fernet(k) for k in keys]
        return True, MultiFernet(fernet_list), "✅ MultiFernet loaded successfully"
    except Exception as e:
        return False, None, f"❌ Failed to load encryption keys: {str(e)}"


def rotate_encryption_key(project_path: str) -> Tuple[bool, str]:
    """Perform full automated key rotation: prepend a brand-new key and migrate every .enc file.
    This is the core of automated rotation and is called automatically when needed.
    """
    new_key = Fernet.generate_key()
    existing_keys = _load_all_keys(project_path)

    # Prepend newest key (encryption always uses the first key)
    all_keys = [new_key] + existing_keys

    try:
        _save_all_keys(project_path, all_keys)

        # Re-encrypt every .enc file using MultiFernet.rotate()
        squishes_dir = os.path.join(project_path, "squishes")
        if not os.path.exists(squishes_dir):
            return True, "✅ New key generated (no .enc files to rotate yet)"

        multifernet = MultiFernet([Fernet(k) for k in all_keys])
        rotated_count = 0
        for filename in os.listdir(squishes_dir):
            if filename.endswith(".enc"):
                enc_path = os.path.join(squishes_dir, filename)
                with open(enc_path, "rb") as f:
                    token = f.read()
                rotated = multifernet.rotate(token)
                with open(enc_path, "wb") as f:
                    f.write(rotated)
                rotated_count += 1

        return True, f"✅ Automated key rotation complete — {rotated_count} .enc files migrated to new key"
    except Exception as e:
        return False, f"❌ Key rotation failed: {str(e)}"


def encrypt_data(data: bytes, project_path: str) -> Tuple[bool, bytes | None, str]:
    """Encrypt raw bytes using the primary (newest) key.
    Automatically triggers rotation if the key is too old.
    """
    # AUTOMATED ROTATION TRIGGER — the magic happens here
    rotated, rot_msg = auto_rotate_if_needed(project_path)
    if not rotated:
        return False, None, rot_msg

    success, multifernet, msg = get_multifernet(project_path)
    if not success:
        return False, None, msg

    try:
        return True, multifernet.encrypt(data), "✅ Data encrypted with current primary key"
    except Exception as e:
        return False, None, f"❌ Encryption failed: {str(e)}"


def decrypt_data(token: bytes, project_path: str) -> Tuple[bool, bytes | None, str]:
    """Decrypt using any key in the MultiFernet list (full rotation support)."""
    success, multifernet, msg = get_multifernet(project_path)
    if not success:
        return False, None, msg
    try:
        return True, multifernet.decrypt(token), "✅ Data decrypted successfully"
    except InvalidToken:
        return False, None, "❌ Decryption failed: wrong key or corrupted file"
    except Exception as e:
        return False, None, f"❌ Decryption failed: {str(e)}"


def secure_delete_key(project_path: str) -> Tuple[bool, str]:
    """Permanently and securely delete the encryption key file (best-practice overwrite)."""
    key_path = _get_key_path(project_path)
    if not os.path.exists(key_path):
        return True, "✅ No encryption key to delete"

    try:
        with open(key_path, "wb") as f:
            f.write(secrets.token_bytes(128))
        os.remove(key_path)
        return True, "✅ Encryption key securely deleted (new key will be generated on next encrypt)"
    except Exception as e:
        return False, f"❌ Failed to securely delete encryption key: {str(e)}"


def list_encrypted_files(project_path: str) -> List[str]:
    """Return list of .enc files in squishes/ ready for decryption."""
    squishes_dir = os.path.join(project_path, "squishes")
    if not os.path.exists(squishes_dir):
        return []
    return [f for f in os.listdir(squishes_dir) if f.endswith(".enc")]
