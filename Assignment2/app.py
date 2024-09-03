from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from tkinter import messagebox
import mariadb
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    conn = mariadb.connect(
        user="root",
        password="tpc12351744",
        host="localhost",
        database="USER_SYSTEM"
    )
    return conn


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        conn.commit()
    except mariadb.IntegrityError:
        return "Username already exists", 400
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        if check_password_hash(user[1], password):
            session['user_id'] = user[0]
            if 'remember_me' in request.form:
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for('dashboard'))
        else:
            messagebox.showwarning("", "Wrong Password")
            return redirect(url_for('index'))
    else:
        messagebox.showwarning("", "Invalid Username")
        return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
