from cryptography.fernet import Fernet
import json, os

FILE = "vault.dat"

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists("key.key"):
        return generate_key()
    with open("key.key", "rb") as f:
        return f.read()

key = load_key()
fernet = Fernet(key)

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "rb") as f:
            decrypted = fernet.decrypt(f.read()).decode()
            return json.loads(decrypted)
    return {}

def save_data(data):
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(FILE, "wb") as f:
        f.write(encrypted)

def add_password(site, password):
    data = load_data()
    data[site] = password
    save_data(data)
    print(f"✅ Saved password for {site}")

def view_passwords():
    data = load_data()
    if not data:
        print("❌ No passwords saved.")
        return
    for site, pwd in data.items():
        print(f"{site}: {pwd}")

def main():
    while True:
        print("\n=== Password Manager ===")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            site = input("Website: ")
            pwd = input("Password: ")
            add_password(site, pwd)
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
