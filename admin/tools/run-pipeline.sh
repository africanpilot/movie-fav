#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# run from root
if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

echo " "
echo "******************************"
echo "STEP 1/3: Running server tests"
echo "******************************"
echo " "

source admin/tools/run-test-server.sh

echo " "
echo "******************************"
echo "STEP 2/3: Running client tests"
echo "******************************"
echo " "

source admin/tools/run-test-client.sh


# TODO: anyother tests to run for db and api directories


# build docker files and push to aws repo
echo " "
echo "******************************"
echo "STEP 3/3: Pushing to aws erc"
echo "******************************"
echo " "

source admin/tools/run-push-erc.sh


echo " "
echo "******************************"
echo "Done run-pipeline.sh"
echo "******************************"
echo " "
