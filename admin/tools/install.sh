#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

########## For local dev only without docker ####################
tools_location=admin/tools

# 1) Setup env

# By default overide db to be local
sed -i "/DB_LOCAL_HOST/c\DB_LOCAL_HOST=localhost" .env
export $(grep -v '^#' .env | xargs)

# 2) Setup pyenv
source $tools_location/install-server-env.sh

# 3) Setup apollo
source $tools_location/install-api-env.sh

# 3) Setup client
source $tools_location/install-client-env.sh

echo " "
echo "******************************"
echo "Done install.sh"
echo "******************************"
echo " "