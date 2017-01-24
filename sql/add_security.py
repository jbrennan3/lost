import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def main():
    cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s);", ("U", "SENSITIVE BUT UNCLASSIFIED"))
    cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s);", ("S", "SECRET"))
    cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s);", ("TS", "TOP SECRET"))
    cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s);", ("SS", ""))
    cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s, %s);", ("Z", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("MOON", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("ADM", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("VOLT", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("ET", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("LGM", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("WPN", ""))
    cur.execute("INSERT INTO compartments (abbrv, comment) VALUES (%s, %s);", ("NRG", ""))
    conn.commit()
    cur.close()
    conn.close()

main()
