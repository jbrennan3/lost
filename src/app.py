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
        if CORRECTLOGIN:
            SQL = "SELECT role FROM user_accounts WHERE username=%s;"
            DATA = (username,)
            cur.execute(SQL, DATA)
            session['role'] = cur.fetchone()[0]
            session['valid'] = 1
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            message = "Username and/or Password incorrect."
            return render_template('error.html', message=message)
        
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
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
                SQL = "INSERT INTO user_accounts (username, password, email, role) VALUES (%s, %s, %s, %s);"
                DATA = (username, password, email, role)
                cur.execute(SQL, DATA)
                conn.commit()
                session['valid'] = 1
                session['username'] = username
                session['role'] = role
                return redirect(url_for('user_created'))
    except:
        pass
    message = "Invalid username or password."
    return render_template('error.html', message = message)
    

@app.route('/user_created', methods=['GET'])
def user_created():
    return render_template('user_created.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'valid' not in session:
        return redirect(url_for('login'))
    else:
        if session['role'] == 'Logistics Officer':
            SQL = "SELECT * FROM in_transit WHERE load_dt = '' OR load_dt = null OR unload_dt = '' OR unload_dt = null;"
            cur.execute(SQL)
            DATA = cur.fetchall()
            dash_results = []
            for line in DATA:
                entry = {}
                entry['val1'] = line[1]
                entry['val2'] = line[2]
                entry['val3'] = line[3]
                entry['val4'] = line[4]
                entry['val5'] = ''
                entry['val6'] = ''

        if session['role'] == 'Facilities Officer':
            SQL = "SELECT * FROM transfer_requests WHERE approver = '' OR approver = null;"
            cur.execute(SQL)
            DATA = cur.fetchall()
            dash_results = []
            for line in DATA:
                entry = {}
                entry['val1'] = line[1]
                entry['val2'] = line[2]
                entry['val3'] = line[3]
                entry['val4'] = line[4]
                entry['val5'] = line[5]
                entry['val6'] = line[6]

        return render_template('dashboard.html');

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    SQL = "SELECT * FROM facilities;"
    cur.execute(SQL)
    DATA = cur.fetchall()
    report_results = []
    for line in DATA:
        entry = {}
        entry['common_name'] = line[1]
        entry['fcode'] = line[2]
        report_results.append(entry)
    session['report_results'] = report_results

    if request.method == 'GET':
        return render_template('add_facility.html')

    if request.method == 'POST':
        if session['role'] == 'Facilities Officer':
            common_name = request.form['common_name'].upper()
            fcode = request.form['fcode'].upper()
            SQL = "SELECT EXISTS(SELECT 1 FROM facilities WHERE common_name=%s OR fcode=%s);"
            cur.execute(SQL, (common_name, fcode))
            DUPLICATE = cur.fetchone()[0]
            if not DUPLICATE:
                SQL = "INSERT INTO facilities (common_name, fcode) VALUES (%s, %s);"
                cur.execute(SQL, (common_name, fcode))
                conn.commit()
                return redirect(url_for('add_facility'))
            else: 
                message = "Duplicate facility detected."
                return render_template('error.html', message = message)
        else:
            message = "insufficient privileges; Facilities Officer required."
            return render_template('error.html', message = message)

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():

    if request.method == 'GET':
        SQL = "SELECT * FROM assets;"
        cur.execute(SQL)
        DATA = cur.fetchall()
        report_results = []
        for line in DATA:
            entry = {}
            entry['asset_tag'] = line[1]
            entry['description'] = line[2]
            report_results.append(entry)
        session['report_results'] = report_results
        return render_template('add_asset.html')

    if request.method == 'POST':
        if session['role'] == 'Logistics Officer':
            asset_tag = request.form['asset_tag'].upper()
            description = request.form['description'].upper()
            facility = request.form['facility'].upper()
            arrive_dt = request.form['arrive_dt']
            SQL = "SELECT EXISTS(SELECT 1 FROM assets WHERE asset_tag=%s);"
            cur.execute(SQL, (asset_tag,))
            DUPLICATE = cur.fetchone()[0]
            if not DUPLICATE:
                try:
                    #I know this section does not have error checking if facility is wrong or fields are missing
                    #I need to add those at some point.
                    SQL = "INSERT INTO assets (asset_tag, description) VALUES (%s, %s) RETURNING asset_pk;"
                    cur.execute(SQL, (asset_tag, description))
                    conn.commit()
                    asset_pk = cur.fetchone()[0]
                    SQL = "SELECT facility_pk FROM facilities WHERE common_name=%s;"
                    cur.execute(SQL, (facility,))
                    facility_pk = cur.fetchone()[0]
                    SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s);"
                    cur.execute(SQL, (asset_pk, facility_pk, arrive_dt))
                    conn.commit()
                    return redirect(url_for('add_asset'))
                except:
                    message = "Invalid and/or Insufficient data entered for asset."
                    return render_template('error.html', message = message )
            else:        
                message = "Duplicate asset detected."
                return render_template('error.html', message = message )

        else:
            message = "insufficient privileges; Logistics Officer required."
            return render_template('error.html', message = message )

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    if session['role'] != 'Logistics Officer':
        message = "insufficient privileges; Logistics Officer required."
        return render_template('error.html', message = message)

    if request.method == 'GET':
        SQL = "SELECT * FROM assets;"
        cur.execute(SQL)
        DATA = cur.fetchall()
        report_results = []
        for line in DATA:
            entry = {}
            entry['asset_tag'] = line[1]
            entry['description'] = line[2]
            report_results.append(entry)
        session['report_results'] = report_results
        return render_template('dispose_asset.html')

    if request.method == 'POST':
        asset_tag = request.form['asset_tag'].upper()
        session['asset_tag'] = asset_tag
        SQL = "SELECT EXISTS(SELECT 1 FROM assets WHERE asset_tag=%s);"
        cur.execute(SQL, (asset_tag,))
        EXISTS = cur.fetchone()[0]
        if EXISTS:
            SQL = "DELETE FROM assets WHERE asset_tag=%s;"
            cur.execute(SQL, (asset_tag,))
            conn.commit()
            return render_template('asset_disposed.html')
    message = "There was a problem with the asset disposal, asset not found or something went very wrong."
    return render_template('error.html', message = message)

@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    if request.method == 'POST':
        facility = request.form['facility'].upper()
        date = request.form['date']
        if facility == "":
            facility = '%'
        if date == "":
            session['asset_results'] = []
            return redirect(url_for('asset_report'))
        SQL = "SELECT common_name, asset_tag, description, arrive_dt FROM facilities f JOIN asset_at aa ON f.facility_pk=aa.facility_fk JOIN assets a ON a.asset_pk=aa.asset_fk WHERE f.common_name LIKE '%" + facility + "%' AND aa.arrive_dt='" + date + "';"
        cur.execute(SQL)
        DATA = cur.fetchall()
        report_results = []
        for line in DATA:
            entry = {}
            entry['facility'] = line[0]
            entry['asset_tag'] = line[1]
            entry['description'] = line[2]
            entry['arrive_dt'] = line[3]
            report_results.append(entry)
        session['asset_results'] = report_results

    return render_template('asset_report.html')

@app.route('/transfer_report', methods=['GET'])
def transfer_report():
    return render_template('transfer_report.html')

@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    if session['role'] != 'Logistics Officer':
        message = "Only Logistics Officers can access request transfers."
        return render_template('error.html', message = message )

    if request.method == 'GET':
        return render_template('transfer_req.html')

    if request.method == 'POST':
        src = request.form['src']
        dest = request.form['dest']
        asset_tag = request.form['asset_tag']
        SQL = "SELECT EXISTS(SELECT 1 FROM facilities f JOIN asset_at aa ON f.facility_pk=aa.facility_fk JOIN assets a ON a.asset_pk=aa.asset_fk WHERE common_name=%s AND asset_tag=%s);"
        cur.execute(SQL, (src, asset_tag))
        EXISTS = cur.fetchone()[0]
        if EXISTS == 0:
            message = "That asset is not at that facility, or that facility does not exist, please check your request again."
            return render_template('error.html', message = message )

        SQL = "SELECT EXISTS(SELECT 1 FROM facilities WHERE common_name=%s);"
        cur.execute(SQL, (dest,))
        EXISTS = cur.fetchone()[0]
        if EXISTS == 0:
            message = "The destination facility is not a valid destination, please check your request again."
            return render_template('error.html', message = message )
        
        requester = session['username']
        SQL = "SELECT facility_pk FROM facilities WHERE common_name=%s;"
        cur.execute(SQL, (src,))
        src_fk = cur.fetchone()[0]
        cur.execute(SQL, (dest,))
        dest_fk = cur.fetchone()[0]
        SQL = "SELECT asset_pk FROM assets WHERE asset_tag=%s;"
        cur.execute(SQL, (asset_tag,))
        asset_fk = cur.fetchone()[0]
        SQL = "INSERT INTO transfer_requests (requester, src_fk, dest_fk, asset_fk) VALUES (%s, %s, %s, %s);"
        cur.execute(SQL, (requester, src_fk, dest_fk, asset_fk))
        conn.commit()
    return render_template('transfer_req.html')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.debug = False
