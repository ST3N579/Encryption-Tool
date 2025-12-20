from cryptography.fernet import Fernet
import sys

def generate_key():
    """Generates a new encryption key."""
    return Fernet.generate_key()

def encrypt_message(message, key):
    """Encrypts a plaintext message using the provided key."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted

def decrypt_message(encrypted_message, key):
    """Decrypts an encrypted message using the provided key."""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_message).decode()
    return decrypted

def main_menu():
    print("\n" + "=" * 50)
    print("         ENCRYPTION/DECRYPTION TOOL")
    print("=" * 50)
    print("  1. Encrypt a message")
    print("  2. Decrypt a message")
    print("  3. Generate a new key")
    print("  4. Exit")
    print("-" * 50)
    choice = input("Choose an option (1-4): ").strip()
    return choice

def print_separator():
    print("-" * 50)

if __name__ == "__main__":
    print("Welcome to the Encryption/Decryption Tool!")
    while True:
        choice = main_menu()
        
        if choice == "1":
            print_separator()
            message = input("Enter the message to encrypt: ").strip()
            key_input = input("Enter encryption key (leave blank to generate new): ").strip()
            if not key_input:
                key = generate_key()
                print(f"\nGenerated key: {key.decode()}")
            else:
                key = key_input.encode()
            try:
                encrypted = encrypt_message(message, key)
                print(f"\nEncrypted message:\n{encrypted.decode()}")
            except Exception as e:
                print(f"\nEncryption failed: {e}")
            print_separator()
        
        elif choice == "2":
            print_separator()
            encrypted_message = input("Enter the encrypted message: ").strip()
            key_input = input("Enter decryption key: ").strip()
            if not key_input:
                print("\nError: Key is required for decryption.")
                print_separator()
                continue
            key = key_input.encode()
            try:
                decrypted = decrypt_message(encrypted_message.encode(), key)
                print(f"\nDecrypted message:\n{decrypted}")
            except Exception as e:
                print(f"\nDecryption failed: {e}")
            print_separator()
        
        elif choice == "3":
            print_separator()
            key = generate_key()
            print(f"\nGenerated key:\n{key.decode()}")
            print_separator()
        
        elif choice == "4":
            print_separator()
            print("Thank you for using the tool. Exiting...")
            break
        
        else:
            print_separator()
            print("Invalid choice. Please select 1-4.")
            print_separator()
        
        input("\nPress Enter to continue...")