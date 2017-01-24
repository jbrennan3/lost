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
            DATA = (line[0].upper(), line[1].upper(), "EXPUNGE DATE: " + line[5].upper())
            cur.execute(SQL, DATA)
            conn.commit()
            asset_pk = cur.fetchone()[0]
            SQL = "SELECT facility_pk FROM facilities WHERE fcode = %s;"
            cur.execute(SQL, facility)
            facility_pk = cur.fetchone()[0]

            try:
                SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s);"
                arrive_dt = line[-2] # what if this is not in 1/12/99 format? ex: Dec-15
                cur.execute(SQL, (asset_pk, facility_pk, arrive_dt))
                conn.commit()
            except:
                SQL = "INSERT INTO asset_at (asset_fk, facility_fk) VALUES (%s, %s);"
                cur.execute(SQL, (asset_pk, facility_pk))
                conn.commit()

            DATA = line[3].upper().replace('"', '')
            DATA = DATA.split(",")
            for element in DATA:
                if element != "":
                    pair = element.split(":")
                    TAG = (pair[0],)
                    LEVEL = (pair[1],)
                    SQL = "SELECT level_pk FROM levels WHERE abbrv = %s;"
                    cur.execute(SQL, LEVEL)
                    level_pk = cur.fetchone()[0]
                    SQL = "SELECT compartment_pk FROM compartments WHERE abbrv = %s;"
                    cur.execute(SQL, TAG)
                    compartment_pk = cur.fetchone()[0]
                    SQL = "INSERT INTO security_tags (level_fk, compartment_fk, asset_fk) VALUES (%s, %s, %s);"
                    cur.execute(SQL, (level_pk, compartment_pk, asset_pk))
                    conn.commit()
            counter += 1
        else:
            counter += 1
    counter = 0
    cur.close()
    conn.close()

main()
