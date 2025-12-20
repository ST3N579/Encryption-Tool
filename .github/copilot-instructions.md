# Copilot Instructions for Encryption Tool

## Architecture Overview
This is a Python-based encryption utility with three interfaces: CLI, GUI, and web app. All interfaces use symmetric encryption via Fernet's AES-based cipher from the `cryptography` library. Core functions (`generate_key`, `encrypt_message`, `decrypt_message`) are duplicated across files rather than shared in a module.

- **encryption_tool.py**: CLI interface with menu-driven encryption/decryption
- **encryption_gui.py**: Tkinter-based desktop GUI
- **encryption_web.py**: Flask web app with Bootstrap UI, runs on port 5000
- **Dockerfile**: Containerizes the web app for deployment

## Key Components
- **Encryption Logic**: Uses `Fernet.generate_key()` for 32-byte keys, `fernet.encrypt(message.encode())` for encryption, `fernet.decrypt()` for decryption. Keys are base64-encoded strings.
- **Error Handling**: Basic try/except blocks catch encryption failures (e.g., invalid key).
- **Dependencies**: Flask 3.0.0 for web, cryptography 42.0.0 for encryption. No other external deps.

## Developer Workflows
- **Run CLI**: `python encryption_tool.py` - interactive menu for encrypt/decrypt/generate key
- **Run GUI**: `python encryption_gui.py` - launches Tkinter window
- **Run Web**: `python encryption_web.py` - starts Flask dev server at http://localhost:5000
- **Docker Build**: `docker build -t encryption-tool .` then `docker run -p 5000:5000 encryption-tool`
- **Debugging**: Web app runs with `debug=True`; check console for Fernet exceptions on invalid keys

## Project Conventions
- **Key Format**: Always base64 string; generate new keys for each session, never reuse for different messages
- **Message Encoding**: Plaintext encoded to bytes before encryption; results decoded back to string for display
- **UI Patterns**: Web app uses inline HTML template with Bootstrap; GUI uses grid layout; CLI uses print/input loops
- **No Shared Code**: Core functions copied verbatim in each file - maintain consistency manually
- **Port**: Web app binds to 0.0.0.0:5000 in Docker, localhost:5000 in dev

## Code Examples
- **Encrypt a message**: `encrypted = Fernet(key).encrypt(b"hello").decode()` (from `encryption_tool.py` line 10)
- **Decrypt**: `decrypted = Fernet(key).decrypt(encrypted.encode()).decode()` (line 15)
- **Generate key**: `key = Fernet.generate_key().decode()` (line 6)
- **Flask route**: Single POST/GET handler in `encryption_web.py` for all actions (line 210)

Focus on Fernet security: keys must be kept secret; use for symmetric encryption only. When adding features, ensure key handling remains secure and consistent across interfaces.