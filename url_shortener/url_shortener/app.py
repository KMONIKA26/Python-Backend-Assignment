from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

# Define the URL model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)

    def __repr__(self):
        return f'<URL {self.short_url}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url(original_url)
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return f'Your short URL is: <a href="/{short_url}">/{short_url}</a>'
    return '''
        <form method="post">
            URL: <input type="text" name="url">
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)

def generate_short_url(original_url):
    hash_object = hashlib.md5(original_url.encode())
    short_hash = hash_object.hexdigest()[:6]
    return short_hash

if __name__ == '__main__':
    app.run(debug=True)
