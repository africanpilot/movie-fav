#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

########## For local dev only without docker ####################
# imports
tools_location=admin/tools
source $tools_location/general-func.sh

# 2) Setup pyenv
install_server_env

# 3) Setup apollo
install_api_env

# 3) Setup client
install_client_env

# 1) Setup env

# validate_service_todo_env
# todo=${SERVICES_TODO}

# for d in $todo; do
#     echo "Adding: $d/.env"
#     export $(grep -v '^#' $d/.env | xargs)
# done
# sed -i "/DB_LOCAL_HOST/c\DB_LOCAL_HOST=localhost" .env
# pass_down_env_copies
# export $(grep -v '^#' .env | xargs)



echo " "
echo "******************************"
echo "Done install.sh"
echo "******************************"
echo " "