#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.


if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

echo " "
echo "******************************"
echo "STEP 1/1: Setting up postgres dependancies"
echo "******************************"
echo " "