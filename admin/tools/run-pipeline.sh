#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# run from root
if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

# imports
tools_location=admin/tools
source $tools_location/general-func.sh

echo " "
echo "******************************"
echo "STEP 1/4: Running server tests"
echo "******************************"
echo " "

# source $tools_location/run-test-server.sh

echo " "
echo "******************************"
echo "STEP 2/4: Running client tests"
echo "******************************"
echo " "

source $tools_location/run-test-client.sh


# TODO: anyother tests to run for db and api directories


# build docker files and push to aws repo
echo " "
echo "******************************"
echo "STEP 3/4: Pushing to aws erc"
echo "******************************"
echo " "

source $tools_location/run-push-erc.sh

# deploy to EC2 instance
echo " "
echo "******************************"
echo "STEP 4/4: Deploy to EC2 instance"
echo "******************************"
echo " "

cd ..
sudo scp -i ${AWS_PEM_FILE_LOCATION} movie-fav/.env ubuntu@${APP_PUBLIC_IP_ADDRESS}:/home/ubuntu/movie-fav
sudo ssh -i ${AWS_PEM_FILE_LOCATION} ubuntu@${APP_PUBLIC_IP_ADDRESS}
cd movie-fav
git stash
git pull https://github.com/africanpilot/movie-fav.git
source run.sh deploy prod down
source run.sh deploy prod build
source run.sh deploy prod up


docker-compose -f server/docker-compose.yml -p services pull

echo " "
echo "******************************"
echo "Done run-pipeline.sh"
echo "******************************"
echo " "