#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# imports
location=admin/tools
source $location/general-func.sh

todo="\
    db/postgres \
    db/redis \
    server \
    api/apollo
"

# db/postgres \
# db/redis \
# server \
# api/apollo \
# client \
# api/nginx \
# api/nginx-apollo \

export SERVICES_TODO="$todo"
script="$1"
environment="$2"
command="$3"
shift 2

# validation process
validate_app_setup

validate_script_agr $script

validate_enviornment_agr $environment

validate_command_agr $command

# set environment variables
sed -i "/APP_DEFULT_ENV/c\APP_DEFULT_ENV=$environment" .env
export $(grep -v '^#' .env | xargs)
pass_down_env_copies

# redirect to script
if [ "$script" == "local" ]; then
    validate_local_setup $todo $location
    source $location/run-local.sh $environment $command
elif [ "$script" == "docker" ]; then
    source $location/run-docker.sh $environment $command
elif [ "$script" == "deploy" ]; then
    aws_erc_login ${AWS_ACCOUNT_ID} ${AWS_REGION}
    source $location/run-deploy.sh $environment $command
else
    echo "Unknown Exception met"
    return 1
fi