import sys
#import pg
#conn = pg.connect(dbname="lost", host="localhost", user="postgres")

def main():
	f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
	print("INSERT INTO facilities (fcode, common_name, location) VALUES (NC, NC Facility, National City)")
	print("INSERT INTO facilities (fcode, common_name, location) VALUES (DC, DC Facility, DC)")
	print("INSERT INTO facilities (fcode, common_name, location) VALUES (HQ, HQ Facility, HQ)")
	print("INSERT INTO facilities (fcode, common_name, location) VALUES (MB005, MB005 Facility, MB005)")
	print("INSERT INTO facilities (fcode, common_name, location) VALUES (SPNV, SPNV Facility, Sparks Nevada)")

main()
