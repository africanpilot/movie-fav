#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.


### this is only necessary when env is local will need to add checker

if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

echo " "
echo "******************************"
echo "STEP 1/1: Setting up server dependancies"
echo "******************************"
echo " "

if [ -d "server/pyenv" ] 
then
    echo "Directory server/pyenv exists."
    source server/pyenv/bin/activate
else
    echo "Directory server/pyenv does not exists. Installing Enviornment"
    python3.10 -m venv server/pyenv
    source server/pyenv/bin/activate
    pip install -r server/requirements.txt
fi

echo " "
echo "******************************"
echo "Done"
echo "******************************"
echo " "