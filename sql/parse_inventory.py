import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()
facility = (sys.argv[4],)

def main():
    f = open(sys.argv[3]) if len(sys.argv) > 1 else sys.stdin
    counter = 0
    for line in f:
        if counter > 0:
            line = line.strip("\n")
            line = line.split(",")
            SQL = "INSERT INTO assets (asset_tag, description, alt_description) VALUES (%s, %s, %s) RETURNING asset_pk;"
            DATA = (line[0].upper(), line[1].upper(), line[3].upper() + " " + line[5].upper())
            cur.execute(SQL, DATA)
            conn.commit()
            asset_pk = cur.fetchone()[0]
            SQL = "SELECT facility_pk FROM facilities WHERE fcode = %s;"
            cur.execute(SQL, facility)
            facility_pk = cur.fetchone()[0]
            SQL = "INSERT INTO asset_at (asset_fk, facility_fk) VALUES (%s, %s);"
            cur.execute(SQL, (asset_pk, facility_pk))
            conn.commit()
            counter += 1
        else:
            counter += 1
    counter = 0
    cur.close()
    conn.close()

main()
