from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import sys

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
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

@app.route('/reports', methods=['POST'])
def reports():
    REPORT = request.form['report']
    ARG = request.form['type']
    FILTER = request.form['filter']
    print(REPORT, ARG, FILTER)
    if REPORT == "asset":
        if ARG == "fac":
            SQL = "SELECT common_name, asset_tag, description, arrive_dt, alt_description FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON f.facility_pk=aa.facility_fk WHERE f.common_name LIKE '%" + FILTER + "%';"
        elif ARG == "date":
            SQL = "SELECT common_name, asset_tag, description, arrive_dt, alt_description FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt LIKE '%" + FILTER + "%';"
        else:
            SQL = "SELECT common_name, asset_tag, description, arrive_dt, alt_description FROM assets a JOIN asset_at aa ON a.asset_pk=aa.asset_fk JOIN facilities f ON f.facility_pk=aa.facility_fk;"
        cur.execute(SQL)
        DATA = cur.fetchall()
        report_results = []
        for line in DATA:
            entry = {}
            entry['common_name'] = line[0]
            entry['asset_tag'] = line[1]
            entry['description'] = line[2]
            entry['arrive_dt'] = line[3]
            entry['alt_description'] = line[4]
            report_results.append(entry)
        session['report_results'] = report_results
        return render_template('asset_report.html')
    if REPORT == "transit":
        SQL = "SELECT * FROM convoys;"
        cur.execute(SQL)
        DATA = cur.fetchall()
        report_results = []
        for line in DATA:
            entry = {}
            entry['request'] = line[1]
            entry['source_fk'] = line[2]
            entry['dest_fk'] = line[3]
            entry['depart_dt'] = line[4]
            entry['arrive_dt'] = line[5]
            report_results.append(entry)
        session['report_results'] = report_results
        return render_template('transit_report.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('logout_page.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.debug = False
