from flask import Flask, request, redirect, render_template_string, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippets.db'
db = SQLAlchemy(app)

# Define the Snippet model
class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    key = db.Column(db.String(256), nullable=True)
    snippet_id = db.Column(db.String(6), unique=True, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

# Generate a random string of 6 characters for the snippet URL
def generate_snippet_id(content):
    hash_object = hashlib.md5(content.encode())
    return hash_object.hexdigest()[:6]

# Encrypt content using a key
def encrypt_content(content, key):
    fernet = Fernet(key)
    return fernet.encrypt(content.encode()).decode()

# Decrypt content using a key
def decrypt_content(content, key):
    fernet = Fernet(key)
    try:
        return fernet.decrypt(content.encode()).decode()
    except InvalidToken:
        return None

# Generate a key from a passphrase (password)
def generate_key_from_passphrase(passphrase):
    return base64.urlsafe_b64encode(hashlib.sha256(passphrase.encode()).digest())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        passphrase = request.form.get('passphrase')

        if passphrase:
            key = generate_key_from_passphrase(passphrase)
            content = encrypt_content(content, key)
        else:
            key = None
        
        snippet_id = generate_snippet_id(content)
        new_snippet = Snippet(content=content, key=key.decode() if key else None, snippet_id=snippet_id)
        db.session.add(new_snippet)
        db.session.commit()

        return f'Shareable URL: <a href="/{snippet_id}">/{snippet_id}</a>'

    return '''
        <form method="post">
            <textarea name="content" placeholder="Enter your snippet"></textarea><br>
            Optional: Enter a passphrase to encrypt your snippet <input type="text" name="passphrase"><br>
            <input type="submit" value="Create Snippet">
        </form>
    '''

@app.route('/<snippet_id>', methods=['GET', 'POST'])
def view_snippet(snippet_id):
    snippet = Snippet.query.filter_by(snippet_id=snippet_id).first_or_404()

    if snippet.key:  # Snippet is encrypted
        if request.method == 'POST':
            passphrase = request.form['passphrase']
            key = generate_key_from_passphrase(passphrase)

            decrypted_content = decrypt_content(snippet.content, key.decode())
            if decrypted_content:
                return f'<h1>Your Snippet:</h1><p>{decrypted_content}</p>'
            else:
                flash('Invalid passphrase, please try again.')
        return '''
            <form method="post">
                <h1>This snippet is encrypted.</h1>
                Enter passphrase: <input type="text" name="passphrase"><br>
                <input type="submit" value="Decrypt">
            </form>
        '''
    else:
        return f'<h1>Your Snippet:</h1><p>{snippet.content}</p>'

if __name__ == '__main__':
    app.run(debug=True)
