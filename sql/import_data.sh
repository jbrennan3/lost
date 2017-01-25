#! /usr/bin/bash
# Take two user arguments $1 and $2
# Database and Port Number
python3 add_facilities.py $1 $2
python3 add_security.py $1 $2
python3 parse_product.py $1 $2 osnap_legacy/product_list.csv
python3 parse_inventory.py $1 $2 osnap_legacy/DC_inventory.csv DC
python3 parse_inventory.py $1 $2 osnap_legacy/HQ_inventory.csv HQ
python3 parse_inventory.py $1 $2 osnap_legacy/MB005_inventory.csv MB005
python3 parse_inventory.py $1 $2 osnap_legacy/NC_inventory.csv NC
python3 parse_inventory.py $1 $2 osnap_legacy/SPNV_inventory.csv SPNV
python3 parse_convoy.py $1 $2 osnap_legacy/convoy.csv
python3 parse_transit.py $1 $2 osnap_legacy/transit.csv
