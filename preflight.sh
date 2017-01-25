#! /usr/bin/bash

# This script handles the setup that must occur prior to running LOST
# Specifically this script:
	# creates the database
	# copies the required source files to $HOME/wsgi

# if no arguments specified, particularly the name of the db throw error
if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit;
fi

# Database prep
cd sql
psql $1 -f create_tables.sql
cd ..

# Install the src to wsgi
cp -R src/* $HOME/wsgi
