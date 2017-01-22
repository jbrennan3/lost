import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def main():
    f = open(sys.argv[3]) if len(sys.argv) > 1 else sys.stdin
    counter = 0
    for line in f:
        if counter > 0:
            line = line.strip("\n")
            line = line.split(",")
            SQL = "INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s);"
            DATA = (line[4].upper(), line[0].upper(), line[1].upper() + " " + line[2].upper())
            cur.execute(SQL, DATA)
            counter += 1
        else:
            counter += 1

    counter = 0
    conn.commit()
    cur.close()
    conn.close()

main()
