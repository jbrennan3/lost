from flask import Flask, render_template, request, redirect, url_for, session
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
        session['username'] = username
        session['password'] = password

    return render_template('main.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('logout_page.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.debug = False
