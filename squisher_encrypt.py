import os
from squisher import create_squish
from squisher_keylogic import (
    generate_encryption_key,
    auto_rotate_if_needed,
    encrypt_data,
    list_encrypted_files
)

def encrypt_squish(project_path: str, project_name: str) -> tuple[bool, str]:
    """Create a fresh squish (zip) then encrypt it with AES-256 using automated key rotation.

    This is now the single public entry point for the entire "Encrypt & Key" feature.
    All key management, rotation, and encryption logic lives in squisher_keylogic.py.
    """
    # Ensure we have a valid key (and rotate automatically if needed)
    success, msg = generate_encryption_key(project_path)
    if not success:
        return False, msg

    rotated, rot_msg = auto_rotate_if_needed(project_path)
    if not rotated:
        return False, rot_msg

    # Create the clean squish first
    squish_success, squish_msg = create_squish(project_path, project_name)
    if not squish_success:
        return False, f"❌ Squish failed before encryption: {squish_msg}"

    # Locate the newest .zip in squishes/
    squishes_dir = os.path.join(project_path, "squishes")
    zip_files = [f for f in os.listdir(squishes_dir) if f.endswith(".zip")]
    if not zip_files:
        return False, "❌ No squish zip found to encrypt"

    latest_zip = max(
        [os.path.join(squishes_dir, f) for f in zip_files],
        key=os.path.getmtime
    )
    zip_filename = os.path.basename(latest_zip)

    # Read the zip and encrypt using the centralized logic
    try:
        with open(latest_zip, "rb") as f:
            data = f.read()

        enc_success, encrypted, enc_msg = encrypt_data(data, project_path)
        if not enc_success:
            return False, enc_msg

        # Save the encrypted file next to the original zip
        enc_filename = zip_filename.replace(".zip", ".enc")
        enc_path = os.path.join(squishes_dir, enc_filename)

        with open(enc_path, "wb") as f:
            f.write(encrypted)

        return True, f"✅ Encrypted {zip_filename} → {enc_filename} (secure AES-256 with auto-rotation)"
    except Exception as e:
        return False, f"❌ Encryption failed: {str(e)}"


# Public utilities still exposed for GUI and other modules
def list_encrypted_files(project_path: str) -> list[str]:
    """Return list of .enc files available for decryption (delegates to keylogic)."""
    return list_encrypted_files(project_path)
