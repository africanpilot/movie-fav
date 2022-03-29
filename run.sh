#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

set -e

# imports
location=admin/tools
source $location/general-func.sh

todo="\
    db/postgres \
    db/redis \
    server \
    api/apollo \
    client \
    api/nginx-apollo
"

# db/postgres \
# db/redis \
# server \
# api/apollo \
# client \
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
sed -i "/APP_DEFAULT_ENV/c\APP_DEFAULT_ENV=$environment" .env
if [ "$script" == "local" ]; then
    sed -i "/APP_DEFAULT_ENV/c\APP_DEFAULT_ENV=local" .env
    if [ "$command" == "down" ]; then
        set +e
    fi
fi
export $(grep -v '^#' .env | xargs)
pass_down_env_copies

# redirect to script
if [ "$script" == "local" ]; then
    prep_for_dev
    validate_local_setup $todo $location
    source $location/run-local.sh $environment $command
elif [ "$script" == "docker" ]; then
    prep_for_dev
    source $location/run-docker.sh $environment $command
elif [ "$script" == "deploy" ]; then
    prep_for_deploy
    aws_erc_login ${AWS_ACCOUNT_ID} ${AWS_REGION}
    source $location/run-deploy.sh $environment $command
elif [ "$script" == "pipeline" ]; then
    if [ "$command" == "up" ] && [ "$environment" == "prod" ]; then 
        prep_for_deploy
        source $location/run-pipeline.sh
    else
        echo "WARNING ERROR: Only pipeline prod up command allowed for pipeline script"
        return 1 
    fi
else
    echo "Unknown Exception met"
    return 1
fi

$SHELL