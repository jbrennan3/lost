from flask import Flask, render_template, request, redirect, url_for, session
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2

conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        SQL = 'SELECT EXISTS(SELECT 1 FROM user_accounts WHERE username=%s AND password=%s);'
        DATA = (username, password)
        cur.execute(SQL, DATA)
        CORRECTLOGIN = cur.fetchone()[0]
        print(CORRECTLOGIN)
        if CORRECTLOGIN:
            session['valid'] = 1
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login_error'))
        
    return render_template('index.html')

@app.route('/login_error', methods=['GET'])
def login_error():
    return render_template('login_error.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('valid', None)
    return render_template('logout_page.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')

    username = request.form['username']
    password = request.form['password']
    email    = request.form['email']
    role     = request.form['role']

    try:
        if len(username) < 17:
            if len(password) < 17:
                print(username, password, email, role)
                SQL = "INSERT INTO user_accounts (username, password, email, role) VALUES (%s, %s, %s, %s);"
                DATA = (username, password, email, role)
                cur.execute(SQL, DATA)
                conn.commit()
                session['valid'] = 1
                session['username'] = username
                return redirect(url_for('user_created'))
    except:
        pass

    return redirect(url_for('user_error'))
    

@app.route('/user_error', methods=['GET'])
def user_error():
    return render_template('user_error.html')

@app.route('/user_created', methods=['GET'])
def user_created():
    return render_template('user_created.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'valid' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html');

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.debug = False
