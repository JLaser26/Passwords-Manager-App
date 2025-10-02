import os
import json
import hashlib
import pyperclip
from cryptography.fernet import Fernet
from password_generator import GenNewPassword

# ======================
# File Paths
# ======================
KEY_FILE = "secret.key"
VAULT_FILE = "vault.json"
MASTER_FILE = "master.hash"

# ======================
# Master Password
# ======================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def setup_master_password():
    if not os.path.exists(MASTER_FILE):
        print("🔐 No master password found. Let's set one up.")
        pw1 = input("Enter new master password: ").strip()
        pw2 = input("Confirm master password: ").strip()
        if pw1 != pw2:
            print("⚠️ Passwords do not match. Try again.")
            return setup_master_password()
        with open(MASTER_FILE, "w") as f:
            f.write(hash_password(pw1))
        print("✅ Master password set successfully!")

def verify_master_password():
    if not os.path.exists(MASTER_FILE):
        setup_master_password()
    with open(MASTER_FILE, "r") as f:
        stored_hash = f.read().strip()
    entered = input("Enter master password: ").strip()
    if hash_password(entered) != stored_hash:
        print("❌ Incorrect master password! Exiting...")
        exit(1)
    print("✅ Master password verified!")

# ======================
# Encryption Setup
# ======================
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    else:
        with open(KEY_FILE, "rb") as f:
            return f.read()

key = load_key()
cipher = Fernet(key)

# ======================
# Vault Storage
# ======================
def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vault(data):
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ======================
# Core Functions
# ======================
def add_account():
    service = input("Enter service/site name (e.g. gmail, github): ").lower().strip()
    username = input("Enter username/email: ").strip()

    choice = input("Do you want to (G)enerate a password or (M)anually enter? [G/M]: ").lower().strip()

    if choice == "g":
        try:
            nuc = int(input("Minimum uppercase letters: "))
            nlc = int(input("Minimum lowercase letters: "))
            ni = int(input("Minimum numbers: "))
            ns = int(input("Minimum symbols: "))
            total = int(input("Total password length: "))
            password = GenNewPassword(nuc, nlc, ni, ns, total)
            print(f"✅ Generated Password: {password}")
        except Exception:
            print("⚠️ Invalid input, try again.")
            return
    else:
        password = input("Enter your password: ").strip()

    vault = load_vault()
    encrypted_pw = cipher.encrypt(password.encode()).decode()
    vault[service] = {"username": username, "password": encrypted_pw}
    save_vault(vault)

    print(f"✅ Account for '{service}' saved successfully!")

def get_account():
    service = input("Enter service/site name to retrieve: ").lower().strip()
    vault = load_vault()

    if service not in vault:
        print("⚠️ No such account found.")
        return

    entry = vault[service]
    decrypted_pw = cipher.decrypt(entry["password"].encode()).decode()

    print("\n🔑 Account Details")
    print(f"Service:   {service}")
    print(f"Username:  {entry['username']}")
    print(f"Password:  {decrypted_pw}")

    choice = input("Copy password to clipboard? [Y/N]: ").lower().strip()
    if choice == "y":
        pyperclip.copy(decrypted_pw)
        print("📋 Password copied to clipboard!")

def list_accounts():
    vault = load_vault()
    if not vault:
        print("⚠️ Vault is empty.")
        return
    print("\n📂 Saved Accounts:")
    for service in vault.keys():
        print(f"- {service}")

def delete_account():
    service = input("Enter service/site name to delete: ").lower().strip()
    vault = load_vault()

    if service not in vault:
        print("⚠️ No such account found.")
        return

    confirm = input(f"Are you sure you want to delete '{service}'? [Y/N]: ").lower().strip()
    if confirm == "y":
        del vault[service]
        save_vault(vault)
        print(f"🗑️ Account '{service}' deleted.")
    else:
        print("❌ Deletion cancelled.")

def update_password():
    service = input("Enter service/site name to update password: ").lower().strip()
    vault = load_vault()

    if service not in vault:
        print("⚠️ No such account found.")
        return

    choice = input("Do you want to (G)enerate a new password or (M)anually enter? [G/M]: ").lower().strip()
    if choice == "g":
        nuc = int(input("Minimum uppercase letters: "))
        nlc = int(input("Minimum lowercase letters: "))
        ni = int(input("Minimum numbers: "))
        ns = int(input("Minimum symbols: "))
        total = int(input("Total password length: "))
        new_pw = GenNewPassword(nuc, nlc, ni, ns, total)
        print(f"✅ Generated Password: {new_pw}")
    else:
        new_pw = input("Enter new password: ").strip()

    vault[service]["password"] = cipher.encrypt(new_pw.encode()).decode()
    save_vault(vault)
    print(f"🔄 Password for '{service}' updated successfully!")

# ======================
# Main Menu
# ======================
def main():
    verify_master_password()

    while True:
        print("\n===== Password Manager =====")
        print("1. Add Account")
        print("2. Get Account")
        print("3. List Accounts")
        print("4. Delete Account")
        print("5. Update Password")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_account()
        elif choice == "2":
            get_account()
        elif choice == "3":
            list_accounts()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            update_password()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
