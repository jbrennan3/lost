#! /usr/bin/bash

function pause(){
    read -p "$*"
}

git clone https://github.com/postgres/postgres.git
cd postgres
#pause 'Postgres downloaded press [Enter] to update to 9.5'
git checkout -b REL9_5_STABLE origin/REL9_5_STABLE
git pull
./configure --prefix=$1/installed
#pause 'Postgres updated press [Enter] to install build.'
make
make install
cd ../
echo Postgres finished.
#pause 'Press [Enter] to continue with Apache setup.'
curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2
cd httpd-2.4.25
#pause 'Apache downloaded press [Enter] to continue with install build.'
./configure --prefix=$1/installed
make
make install
cd ../
#cd $1/installed/bin
#mkdir data
#./initdb -D data
#cd -
echo ~~~~~~~~~~~~~~~~~~ Install Complete ~~~~~~~~~~~~~~~~~~~~~~~~~
echo Make sure to change Apache Server listen port to desired port.
echo Apache and Postgres installed to $1/installed.
echo Postgres Database located at $1/installed/bin/data
