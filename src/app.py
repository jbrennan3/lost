from flask import Flask, render_template, request, redirect, url_for, session
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2

conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route('/rest')
def rest():
    return render_template('rest.html', dbname=dbname, dbhost=dbhost, dbport=dbport)

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

@app.route('/rest/list_products', methods=('POST',))
def list_products():
    """This function is huge... much of it should be broken out into other supporting
        functions"""
    
    # Check maybe process as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    # Unmatched, take the user somewhere else
    else:
        redirect('rest')
    
    # If execution gets here we have request json to work with
    # Do I need to handle compartments in this query?
    if len(req['compartments'])==0:
        print("have not compartment")
        # Just handle vendor and description
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from products p
left join security_tags t on p.product_pk=t.product_fk
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        # Need to handle compartments too
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from security_tags t
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    # One of the 8 cases should've run... process the results
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)

    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)
    
    conn.close()
    return data
    
@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/activate_user', methods=('POST',))
def activate_user():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/add_products', methods=('POST', ))
def add_products():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.debug = False
