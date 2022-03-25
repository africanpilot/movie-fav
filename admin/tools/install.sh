#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# go up to root dir
# cd ../../
# set -e

if set|grep '^SERVICES_TODO=' >/dev/null; then
  todo="$SERVICES_TODO"
else
  echo "Please set the SERVICES_TODO env"
  return 1
fi

if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

########## For local dev only without docker ####################3

# 1) Run the .env files

echo " "
echo "******************************"
echo "STEP 1/5: Setting enviornment varables"
echo "******************************"
echo " "

# for d in $(find . -maxdepth 3 -name "*.env"); do
#     echo "Adding: $d"
#     # update .env file for match dev setting
#     # sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=local' $d
#     sed -i '/DB_LOCAL_HOST/c\DB_LOCAL_HOST=localhost' $d
#     # Show env vars
#     # grep -v '^#' $d

#     # Export env vars
#     export $(grep -v '^#' $d | xargs)
# done

for d in $todo; do
    echo "Adding: $d/.env"
    export $(grep -v '^#' $d/.env | xargs)
done

# By default overide db to be local
export DB_LOCAL_HOST=localhost


# 2) Setup pyenv

echo " "
echo "******************************"
echo "STEP 2/5: Setting up server python enviornment"
echo "******************************"
echo " "

if [ -d "server/pyenv" ] 
then
    echo "Directory server/pyenv exists."
    source server/pyenv/bin/activate
else
    echo "Directory server/pyenv does not exists. Installing Enviornment"
    python3 -m venv server/pyenv
    source server/pyenv/bin/activate
    pip install -r server/requirements.txt
fi

# 3) Setup apollo

echo " "
echo "******************************"
echo "STEP 3/5: Setting up apollo packages"
echo "******************************"
echo " "

if [ -d "api/apollo/node_modules" ] 
then
    echo "Directory api/apollo/node_modules exists."
else
    echo "Directory api/apollo/node_modules does not exists. Installing Enviornment"
    npm --prefix api/apollo install
fi

# 3) Setup client

echo " "
echo "******************************"
echo "STEP 4/5: Setting up client packages"
echo "******************************"
echo " "

if [ -d "client/node_modules" ] 
then
    echo "Directory client/node_modules exists."
else
    echo "Directory client/node_modules does not exists. Installing Enviornment"
    npm --prefix client install
fi


# 3) Setup postgres database
echo " "
echo "******************************"
echo "STEP 5/5: Setting up postgres database"
echo "******************************"
echo " "



echo "Done."
echo "******************************"
echo " "