import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

def main():
    f = open(sys.argv[3]) if len(sys.argv) > 1 else sys.stdin
    counter = 0
    dict = { 'MB 005': 'MB005', 'Headquarters': 'HQ', 'Site 300': 'ST', 'National City': 'NC', ',Groom Lake,': 'GL', 'Sparks, NV': 'SPNV', 'Los Alamos, NM': 'LA', 'Washington, D.C.': 'DC', 'Los Alamous, NM': 'LA', 'Las Alamos, NM': 'LA' }
    for line in f:
        if counter > 0:
            transit = line.strip("\n")
            line = line.strip("\n")
            line = line.split(",")
            request_num = line[-2]
            transit = transit.split(chr(34))
            del transit[0]
            if transit[0].startswith('CA'):
                del transit[0]
            if counter < 3:
                transit = transit[0].split(",")
                src = transit[1]
                dest = transit[2]
            else:
                for e in transit:
                    if e == ",":
                        transit.remove(e)
                src = transit[0]
                dest = transit[1]

            SQL = "UPDATE convoys set source_fk=f.facility_pk FROM facilities f WHERE f.fcode='" + dict[src] + "' AND convoys.request='" + request_num + "';"
            cur.execute(SQL)
            conn.commit()

            SQL = "UPDATE convoys set dest_fk=f.facility_pk FROM facilities f WHERE f.fcode='" + dict[dest] + "' AND convoys.request='" + request_num + "';"
            cur.execute(SQL)
            conn.commit()

            counter += 1
        else:
            counter += 1
    cur.close()
    conn.close()

main()
