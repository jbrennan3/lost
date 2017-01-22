import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def main():
    cur.execute("INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);", ("NC", "NC Facility", "National City"))
    cur.execute("INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);", ("DC", "DC Facility", "DC"))
    cur.execute("INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);", ("HQ", "HQ Facility", "HQ"))
    cur.execute("INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);", ("MB005", "MB005 Facility", "MB005"))
    cur.execute("INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);", ("SPNV", "SPNV Facility", "Sparks Nevada"))
    conn.commit()
    cur.close()
    conn.close()

main()
