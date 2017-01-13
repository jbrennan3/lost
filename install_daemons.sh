#! /usr/bin/bash

function pause(){
    read -p "$*"
}

PATH=$1
if [ $# -eq 0 ]
    then PATH=$HOME
fi

#pause 'Install path to ' $PATH '? Press [Enter] to continue or Ctrl + C to exit.'

git clone https://github.com/postgres/postgres.git
#pause 'Postgres downloaded press [Enter] to update to 9.5'
cd postgres
git checkout -b REL9_5_STABLE origin/REL9_5_STABLE
git pull
./configure --prefix=$PATH/installed

#pause 'Postgres updated press [Enter] to install build.'
make
make install
cd ../

#pause 'Press [Enter] to continue with Apache setup.'
curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2

#pause 'Apache downloaded press [Enter] to continue with install build.'
cd httpd-2.4.25
./configure --prefix=$PATH/installed
make
make install
cd ../

echo ~~~~~~~~~~~~~~~~~~ Install Complete ~~~~~~~~~~~~~~~~~~~~~~~~~
echo Make sure to change Apache Server listen port to desired port.
echo Apache and Postgres installed to $PATH/installed.
