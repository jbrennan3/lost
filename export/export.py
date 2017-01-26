#! /usr/bin/python3

import csv
import psycopg2
import sys

try:
    conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
except:
    conn = psycopg2.connect(dbname=sys.argv[1], host='/tmp', port=5432)

cur = conn.cursor()
datapath = sys.argv[2]

def main():
    #USERS.CSV
    SQL = "SELECT * from user_accounts;"
    cur.execute(SQL)
    results = cur.fetchall()
    with open(datapath + '/users.csv', "w") as csvfile:
            fieldnames = ['username', 'password', 'role', 'active']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow({'username': row[0], 'password': row[1], 'role': row[2], 'active': row[3]}) 

    #FACILITIES.CSV
    SQL = "SELECT * from facilities;"
    cur.execute(SQL)
    results = cur.fetchall()
    with open(datapath + '/facilities.csv', "w") as csvfile:
            fieldnames = ['fcode', 'common_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow({'fcode' : row[1], 'common_name': row[2]}) 

    #ASSETS.CSV
    SQL = "SELECT asset_tag, description, fcode, arrive_dt, dispose_dt FROM facilities f JOIN asset_at aa ON f.facility_pk=aa.facility_fk JOIN assets a ON a.asset_pk=aa.asset_fk;"
    cur.execute(SQL)
    results = cur.fetchall()
    with open(datapath + '/assets.csv', "w") as csvfile:
            fieldnames = ['asset_tag', 'description', 'facility', 'acquired', 'disposed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow({'asset_tag' : row[0], 'description': row[1], 'facility': row[2], 'acquired': row[3], 'disposed': row[4]}) 

    #TRANSFERS.CSV
    SQL = "SELECT asset_tag, requester, request_dt, approver, approve_dt, fcode, it.dest_fk, load_dt, unload_dt FROM transfer_requests tr JOIN assets a ON tr.asset_fk=a.asset_pk JOIN facilities f ON tr.src_fk=f.facility_pk JOIN in_transit it ON it.asset_fk=a.asset_pk;"
    cur.execute(SQL)
    results = cur.fetchall()
    with open(datapath + '/transfers.csv', "w") as csvfile:
            fieldnames = ['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                SQL = "SELECT fcode FROM facilities WHERE facility_pk=%s;"
                cur.execute(SQL, (row[6],))
                dest = cur.fetchone()[0]
                writer.writerow({'asset_tag' : row[0], 'request_by': row[1], 'request_dt': row[2], 'approve_by': row[3], 'approve_dt': row[4], 'source': row[5], 'destination': dest, 'load_dt': row[7], 'unload_dt': row[8]}) 

main()
