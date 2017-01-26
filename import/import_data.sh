#! /usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <input dir>"
	exit;
fi
python3 import.py $1 $2
