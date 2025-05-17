from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import psutil
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret in production

# Initialize DB
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
        conn.close()

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return render_template('register.html', error='Username already exists.')
        else:
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login_page'))

    return render_template('register.html')

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    alerts = []
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            if p_info['cpu_percent'] > 50 or p_info['memory_percent'] > 10:
                alerts.append(f"⚠️ High usage: {p_info['name']} (CPU: {p_info['cpu_percent']}%, Memory: {p_info['memory_percent']:.2f}%)")
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return render_template('dashboard.html', username=session['username'], alerts=alerts, processes=processes)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

# Run App
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
