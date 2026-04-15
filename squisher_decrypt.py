import os
from squisher_keylogic import decrypt_data, list_encrypted_files

def decrypt_squish(enc_path: str, project_path: str) -> tuple[bool, str]:
    """Decrypt a specific .enc file back to a usable .zip using the current MultiFernet.

    Fully supports automated key rotation — any past key will still decrypt correctly.
    Places the decrypted zip in the same squishes/ folder with a clear _decrypted suffix.
    """
    if not os.path.exists(enc_path):
        return False, "❌ Encrypted file not found"

    # Read the encrypted token
    try:
        with open(enc_path, "rb") as f:
            token = f.read()
    except Exception as e:
        return False, f"❌ Could not read encrypted file: {str(e)}"

    # Use centralized decryption (handles rotation automatically)
    success, decrypted, msg = decrypt_data(token, project_path)
    if not success:
        return False, msg

    # Save the decrypted zip next to the original .enc
    output_path = enc_path.replace(".enc", "_decrypted.zip")
    try:
        with open(output_path, "wb") as f:
            f.write(decrypted)
        return True, f"✅ Decrypted to {os.path.basename(output_path)} (ready to unzip)"
    except Exception as e:
        return False, f"❌ Failed to write decrypted file: {str(e)}"


def decrypt_latest_squish(project_path: str) -> tuple[bool, str]:
    """Convenience helper: decrypt the most recent .enc file in squishes/ (for one-click future GUI use)."""
    enc_files = list_encrypted_files(project_path)
    if not enc_files:
        return False, "❌ No encrypted archives found in squishes/"

    # Sort by modification time and pick the newest
    squishes_dir = os.path.join(project_path, "squishes")
    latest_enc = max(
        [os.path.join(squishes_dir, f) for f in enc_files],
        key=os.path.getmtime
    )
    return decrypt_squish(latest_enc, project_path)


# Public utilities still exposed
def list_encrypted_files(project_path: str) -> list[str]:
    """Return list of .enc files available for decryption (delegates to keylogic)."""
    return list_encrypted_files(project_path)
