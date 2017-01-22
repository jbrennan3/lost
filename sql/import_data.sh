#! /usr/bin/bash
# Take two user arguments $1 and $2
# Database and Port Number
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar.gz
psql -d $1 -a -f create_tables.sql
python3 add_facilities.py $1 $2
python3 parse_product.py $1 $2 osnap_legacy/product_list.csv
python3 parse_inventory.py $1 $2 osnap_legacy/DC_inventory.csv DC
python3 parse_inventory.py $1 $2 osnap_legacy/HQ_inventory.csv HQ
python3 parse_inventory.py $1 $2 osnap_legacy/MB005_inventory.csv MB005
python3 parse_inventory.py $1 $2 osnap_legacy/NC_inventory.csv NC
python3 parse_inventory.py $1 $2 osnap_legacy/SPNV_inventory.csv SPNV
rm -rf osnap_legacy/
rm -rf osnap_legacy.tar.gz
