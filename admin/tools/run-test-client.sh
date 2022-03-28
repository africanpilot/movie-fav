#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# run from root
if [  ! -d "client" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

# imports
tools_location=admin/tools
source $tools_location/general-func.sh

echo " "
echo "******************************"
echo "STEP 1/2: Starting test enviornment"
echo "******************************"
echo " "

# TODO: for later

echo " "
echo "******************************"
echo "Done run-test-client.sh"
echo "******************************"
echo " "