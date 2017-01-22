This functionality is dependent upon the psql data directory and desired database created.

Instructions: ensure psql server started and run the bash script supplying the name of the database and
the port number.  example: ./import_data.sh myDataBase 5432

Files:
	import_data.sh - BASH script to download and import legacy data.

Dependencies:
	create_tables.sql - SQL to create the LOST database tables.
	add_facilities.py - Python script to populate facility tables.
	parse_product.py - Python script to populate product information.
	parse_inventory.py - Python script to populate existing inventory.
