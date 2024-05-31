from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from app import app


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your database username
app.config['MYSQL_PASSWORD'] = 'password'  # Change to your database password
app.config['MYSQL_DB'] = 'moodmatch'

mysql = MySQL(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'full_name' in request.form and 'email' in request.form and 'password' in request.form:
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not full_name or not email or not password:
            flash('Please fill out the form!')
        else:
            cursor.execute('INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)', (full_name, email, password,))
            mysql.connection.commit()
            flash('You have successfully registered!')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['full_name'] = account['full_name']
            return redirect(url_for('index'))
        else:
            flash('Incorrect email/password!')

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('full_name', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('index.html', full_name=session['full_name'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
