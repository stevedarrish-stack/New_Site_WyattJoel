 
from flask import Flask, render_template, request, g, redirect, url_for, session, flash
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret_key'  # Change this in production
DATABASE = os.path.join(os.path.dirname(__file__), 'inquiries.db')

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'  # Change this in production

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Admin login/logout routes
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next') or url_for('view_inquiries')
            return redirect(next_page)
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# Admin inquiries page (protected)
@app.route('/admin/inquiries')
@login_required
def view_inquiries():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, email, message, submitted_at FROM inquiries ORDER BY submitted_at DESC')
    inquiries = cursor.fetchall()
    return render_template('inquiries.html', inquiries=inquiries)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/inquiry', methods=['POST'])
def inquiry():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO inquiries (name, email, message) VALUES (?, ?, ?)',
        (name, email, message)
    )
    db.commit()
    success = f"Thank you, {name}! Your inquiry has been received."
    return render_template('index.html', success=success)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)