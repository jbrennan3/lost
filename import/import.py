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
    with open(datapath + "/users.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            SQL = "INSERT INTO user_accounts (username, password, role, active) VALUES( %s, %s, %s, %s );"
            cur.execute(SQL, (row['username'], row['password'], row['role'], row['active']))
            conn.commit()

    with open(datapath + "/facilities.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            SQL = "INSERT INTO facilities (fcode, common_name) VALUES( %s, %s );"
            cur.execute(SQL, (row['fcode'], row['common_name']))
            conn.commit()

    with open(datapath + "/assets.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            SQL = "INSERT INTO assets (asset_tag, description) VALUES( %s, %s ) RETURNING asset_pk;"
            cur.execute(SQL, (row['asset_tag'], row['description']))
            conn.commit()
            asset_pk = cur.fetchone()[0]
            SQL = "SELECT facility_pk FROM facilities WHERE common_name=%s;"
            cur.execute(SQL, (row['facility'],))
            facility_pk = cur.fetchone()[0]
            SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, dispose_dt) VALUES (%s, %s, %s, %s);"
            cur.execute(SQL, (asset_pk, facility_pk, row['acquired'], row['disposed']))
            conn.commit()

    with open(datapath + "/transfers.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            SQL = "INSERT INTO transfer_requests (requester, src_fk, dest_fk, asset_fk, approver, approval, request_dt, approve_dt) VALUES( %s, %s, %s, %s, %s, %s, %s, %s );"
            cur.execute("SELECT facility_pk FROM facilities WHERE fcode='" + row['source'] +"';")
            src_fk = cur.fetchone()[0]
            cur.execute("SELECT facility_pk FROM facilities WHERE fcode='" + row['destination'] +"';")
            dest_fk = cur.fetchone()[0]
            cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='" + row['asset_tag'] + "';")
            asset_fk = cur.fetchone()[0]
            APPROVAL = 'REJECTED'
            if len(row['load_dt']) > 0:
                APPROVAL = 'APPROVED'
                
            cur.execute(SQL, (row['requester'], src_fk, dest_fk, asset_fk, row['approver'], APPROVAL, row['request_dt'], row['approve_dt']))
            conn.commit()
            SQL = "INSERT INTO in_transit (asset_fk, src_fk, load_dt, dest_fk, unload_dt) VALUES (%s, %s, %s, %s, %s);"
            cur.execute(SQL, (asset_fk, src_fk, row['load_dt'], dest_fk, row['unload_dt']))
            conn.commit()



main()
