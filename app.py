from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management


def get_db():
    conn = sqlite3.connect('data.db')
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/remove_user/<int:user_id>', methods=['POST'])
def remove_user(user_id):
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))  # Redirect to login if not logged in or not admin

    db = get_db()
    cursor = db.cursor()

    # Remove the user by ID
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()

    return redirect(url_for('admin_dashboard'))  # Redirect back to the admin dashboard after deletion


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))  # Redirect to login if not logged in or not admin

    if request.method == 'POST':
        # Get data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        department = request.form['department']
        password = request.form['password']

        # Insert new user into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (firstName, lastName, birthDate, password, department)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, birth_date, password, department))
        db.commit()

        return redirect(url_for('admin_dashboard'))  # Redirect back to admin dashboard after adding

    return render_template('add_user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Query for user credentials
        cursor.execute('''
            SELECT * FROM users WHERE firstName = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Store the user ID in session
            session['is_admin'] = user[1]  # Store admin status in session

            if user[1]:  # If the user is an admin
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            # Invalid login credentials
            return "Invalid username or password, please try again.", 401

    return render_template('login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))  # Redirect to login if not logged in or not admin

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  # Fetch all users from the database

    return render_template('admin_dashboard.html', users=users)


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))  # Redirect to login if not logged in or if admin

    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    return render_template('user_dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.clear()  # Clears the session data
    return redirect(url_for('index'))  # Redirect to homepage


if __name__ == "__main__":
    app.run(debug=True)
