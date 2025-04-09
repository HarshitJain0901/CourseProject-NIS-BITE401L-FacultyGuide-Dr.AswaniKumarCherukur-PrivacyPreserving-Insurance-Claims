from cryptography.fernet import Fernet
import os

def generate_key(path="src/aes.key"):
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)

def load_key(path="src/aes.key"):
    with open(path, "rb") as f:
        return f.read()

def encrypt_file(input_file, output_file, key):
    fernet = Fernet(key)
    with open(input_file, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(output_file, "wb") as f:
        f.write(encrypted)

def decrypt_file(input_file, output_file, key):
    fernet = Fernet(key)
    with open(input_file, "rb") as f:
        encrypted_data = f.read()
    decrypted = fernet.decrypt(encrypted_data)
    with open(output_file, "wb") as f:
        f.write(decrypted)
