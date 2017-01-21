#! /usr/bin/bash
# Take two user arguments $1 and $2
# Database and Port Number
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar.gz
python3 add_facilities.py
python3 parse_product.py < osnap_legacy/product_list.csv
python3 parse_inventory.py < osnap_legacy/DC_inventory.csv
python3 parse_inventory.py < osnap_legacy/HQ_inventory.csv
python3 parse_inventory.py < osnap_legacy/MB005_inventory.csv
python3 parse_inventory.py < osnap_legacy/NC_inventory.csv
python3 parse_inventory.py < osnap_legacy/SPNV_inventory.csv
rm -rf osnap_legacy/
rm -rf osnap_legacy.tar.gz
