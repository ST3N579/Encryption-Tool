from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet

app = Flask(__name__)

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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encryption/Decryption Tool</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%), url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            max-width: 1200px;
            margin-top: 30px;
        }
        .card {
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: none;
            border-radius: 15px;
            overflow: hidden;
            min-height: 400px;
        }
        .card-header {
            background: linear-gradient(45deg, #007bff, #0056b3);
            color: white;
            text-align: center;
            padding: 20px;
        }
        .btn-custom {
            background: linear-gradient(45deg, #007bff, #0056b3);
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .btn-custom:hover {
            background: linear-gradient(45deg, #0056b3, #004085);
            transform: translateY(-2px);
        }
        .btn-success {
            border-radius: 25px;
            font-weight: bold;
        }
        .btn-outline-secondary {
            border-radius: 25px;
        }
        .form-control {
            border-radius: 10px;
            border: 2px solid #ddd;
        }
        .form-control:focus {
            border-color: #007bff;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }
        .alert {
            border-radius: 10px;
            max-height: 300px;
            overflow-y: auto;
        }
        .notes-card {
            height: 100%;
        }
        .notes-textarea {
            resize: vertical;
            min-height: 300px;
        }
        .clear-btn {
            background: linear-gradient(45deg, #dc3545, #c82333);
            border: none;
            border-radius: 25px;
            color: white;
            font-weight: bold;
        }
        .btn-copied {
            background-color: #28a745 !important;
            border-color: #28a745 !important;
            color: white !important;
            transition: all 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2><i class="fas fa-lock"></i> Encryption/Decryption Tool</h2>
                    </div>
                    <div class="card-body">
                        <form method="post">
                            <div class="mb-3">
                                <label for="key" class="form-label"><i class="fas fa-key"></i> Encryption Key</label>
                                <div class="input-group">
                                    <input type="text" class="form-control" id="key" name="key" value="{{ key }}" placeholder="Enter or generate a key">
                                    <button type="submit" name="action" value="generate" class="btn btn-outline-secondary"><i class="fas fa-sync-alt"></i> Generate</button>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="message" class="form-label"><i class="fas fa-envelope"></i> Message</label>
                                <textarea class="form-control" id="message" name="message" rows="5" placeholder="Enter your message here">{{ message }}</textarea>
                            </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                                <button type="submit" name="action" value="encrypt" class="btn btn-custom me-md-2"><i class="fas fa-lock"></i> Encrypt</button>
                                <button type="submit" name="action" value="decrypt" class="btn btn-success"><i class="fas fa-unlock"></i> Decrypt</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card notes-card">
                    <div class="card-header">
                        <h4><i class="fas fa-sticky-note"></i> Notes & Saved Encrypted Text</h4>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <textarea class="form-control notes-textarea mb-3" id="notes" rows="10" placeholder="Save your encrypted messages or notes here...">{{ notes }}</textarea>
                        <button type="button" class="btn clear-btn align-self-start" onclick="clearNotes()"><i class="fas fa-trash"></i> Clear</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-info-circle"></i> Result</h4>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <div class="alert alert-light">
                                <div id="result-text" style="white-space: pre-wrap; font-family: monospace; word-break: break-all;">{{ result_text }}</div>
                                </div>
                            </div>
                            {% if result_text != "No result yet. Encrypt or decrypt a message to see the output here." %}
                            <div class="ms-3">
                                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="copyResult()"><i class="fas fa-copy"></i> Copy</button>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer class="text-center mt-5 text-white">
        <p>&copy; 2025 Created by ST3N579</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function clearNotes() {
            document.getElementById('notes').value = '';
            localStorage.removeItem('notes');
        }
        function copyResult() {
            const text = document.getElementById('result-text').textContent;
            const button = event.target.closest('button');
            navigator.clipboard.writeText(text).then(() => {
                button.classList.add('btn-copied');
                setTimeout(() => {
                    button.classList.remove('btn-copied');
                }, 500);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }
        window.onload = function() {
            const notesTextarea = document.getElementById('notes');
            const savedNotes = localStorage.getItem('notes');
            if (savedNotes) {
                notesTextarea.value = savedNotes;
            }
            notesTextarea.addEventListener('input', function() {
                localStorage.setItem('notes', this.value);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    key = ""
    message = ""
    result = ""
    error = ""
    result_text = "No result yet. Encrypt or decrypt a message to see the output here."

    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key', '').strip()
        message = request.form.get('message', '').strip()

        if action == 'generate':
            try:
                new_key = generate_key()
                key = new_key.decode()
                result_text = "New key generated successfully!"
            except Exception as e:
                result_text = f"Failed to generate key: {e}"
        elif action == 'encrypt':
            if not message:
                result_text = "Please enter a message to encrypt."
            elif not key:
                result_text = "Please provide a key."
            else:
                try:
                    encrypted = encrypt_message(message, key.encode())
                    result_text = encrypted.decode()
                except Exception as e:
                    result_text = f"Encryption failed: {e}"
        elif action == 'decrypt':
            if not message:
                result_text = "Please enter an encrypted message to decrypt."
            elif not key:
                result_text = "Please provide the decryption key."
            else:
                try:
                    decrypted = decrypt_message(message.encode(), key.encode())
                    result_text = decrypted
                except Exception as e:
                    result_text = f"Decryption failed: {e}"

    return render_template_string(HTML_TEMPLATE, key=key, message=message, result_text=result_text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)