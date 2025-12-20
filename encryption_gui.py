import tkinter as tk
from tkinter import messagebox, scrolledtext
from cryptography.fernet import Fernet

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

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption/Decryption Tool")
        self.root.geometry("600x500")

        # Key storage
        self.current_key = None

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Encryption/Decryption Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Key section
        key_frame = tk.Frame(self.root)
        key_frame.pack(pady=10)

        tk.Label(key_frame, text="Encryption Key:").grid(row=0, column=0, sticky="w")
        self.key_entry = tk.Entry(key_frame, width=50)
        self.key_entry.grid(row=0, column=1, padx=5)

        self.generate_key_button = tk.Button(key_frame, text="Generate New Key", command=self.generate_key_action)
        self.generate_key_button.grid(row=0, column=2, padx=5)

        # Message section
        message_frame = tk.Frame(self.root)
        message_frame.pack(pady=10)

        tk.Label(message_frame, text="Message:").grid(row=0, column=0, sticky="nw")
        self.message_text = scrolledtext.ScrolledText(message_frame, width=50, height=5)
        self.message_text.grid(row=0, column=1, padx=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.encrypt_button = tk.Button(button_frame, text="Encrypt", command=self.encrypt_action, width=15)
        self.encrypt_button.grid(row=0, column=0, padx=10)

        self.decrypt_button = tk.Button(button_frame, text="Decrypt", command=self.decrypt_action, width=15)
        self.decrypt_button.grid(row=0, column=1, padx=10)

        # Result section
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10, fill="both", expand=True)

        tk.Label(result_frame, text="Result:").grid(row=0, column=0, sticky="nw")
        self.result_text = scrolledtext.ScrolledText(result_frame, width=50, height=5)
        self.result_text.grid(row=0, column=1, padx=5, sticky="nsew")

        # Configure grid weights
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(1, weight=1)

    def generate_key_action(self):
        try:
            key = generate_key()
            self.current_key = key
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key.decode())
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "New key generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate key: {e}")

    def encrypt_action(self):
        message = self.message_text.get(1.0, tk.END).strip()
        key_str = self.key_entry.get().strip()

        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encrypt.")
            return

        if not key_str:
            messagebox.showwarning("Warning", "Please provide or generate a key.")
            return

        try:
            key = key_str.encode()
            encrypted = encrypt_message(message, key)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, encrypted.decode())
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_action(self):
        encrypted_message = self.message_text.get(1.0, tk.END).strip()
        key_str = self.key_entry.get().strip()

        if not encrypted_message:
            messagebox.showwarning("Warning", "Please enter an encrypted message to decrypt.")
            return

        if not key_str:
            messagebox.showwarning("Warning", "Please provide the decryption key.")
            return

        try:
            key = key_str.encode()
            decrypted = decrypt_message(encrypted_message.encode(), key)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, decrypted)
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()