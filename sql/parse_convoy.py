import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def main():
    f = open(sys.argv[3]) if len(sys.argv) > 1 else sys.stdin
    counter = 0
    for line in f:
        if counter > 0:
            vehicles = line.strip("\n")
            line = line.strip("\n")
            line = line.split(",")
            try:
                vehicles = vehicles.split(chr(34))
                vehicles = vehicles[1].split(",")
                vehicles = [v.lstrip() for v in vehicles]
            except:
                vehicles = [line[7]]


            SQL = "INSERT INTO convoys (request, depart_dt, arrive_dt) VALUES (%s, %s, %s) RETURNING convoy_pk;"
            DATA = (line[0].upper(), line[1].upper(), line[6].upper())
            cur.execute(SQL, DATA)
            conn.commit()
            convoy_pk = cur.fetchone()[0]

            for v in vehicles:
                SQL = "INSERT INTO assets (asset_tag, description) VALUES (%s, %s) RETURNING asset_pk;"
                DATA = (v, "VEHICLE")
                cur.execute(SQL, DATA)
                conn.commit()
                asset_pk = cur.fetchone()[0]
                SQL = "INSERT INTO vehicles (asset_fk) VALUES (%s) RETURNING vehicle_pk;"
                cur.execute(SQL, (asset_pk,))
                conn.commit()
                vehicle_pk = cur.fetchone()[0]
                SQL = "INSERT INTO used_by (vehicle_fk, convoy_fk) VALUES (%s, %s);"
                DATA = (vehicle_pk, convoy_pk)
                cur.execute(SQL, DATA)
                conn.commit()
            

            counter += 1
        else:
            counter += 1
    cur.close()
    conn.close()

main()
