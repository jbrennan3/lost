import sys
#import pg
#conn = pg.connect(dbname="lost", host="localhost", user="postgres")

def main():
	f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
	counter = 0
	for line in f:
		if counter > 0:
			line = line.strip("\n")
			line = line.split(",")
			print("INSERT INTO assets (asset_tag, description, alt_description) VALUES (" + line[0].upper() + ", " + line[1].upper() + ", " + line[3].upper() + " " + line[5].upper() + ")")
			counter += 1
		else:
			counter += 1
	counter = 0

main()
