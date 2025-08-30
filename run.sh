# !/bin/bash

set -e

# imports
tools_location=admin/tools
source $tools_location/general-func.sh

# get args
script="$1"
environment="$2"
command="$3"
target="$4"

# validation process
if [ "$script" = "docker" ] || [ "$script" = "nerdctl" ] || [ "$script" = "deploy" ]; then
    shift 2
    validate_engine $script
    validate_script_agr $script
    validate_enviornment_agr $environment
    validate_command_agr $command
    validate_app_setup $environment
    source .buildx.env

    # set environment variables
    export SERVICES_TODO=""
    export DOCKER_COMPOSE_FILE_NAME="docker-compose-$environment.yml"
    export_env_var $environment

    # update service todo if necessary
    if [ ! -z "$target" ]; then
        export SERVICES_TODO=$target
        echo "service todo update: $SERVICES_TODO"
    fi
fi
# redirect to script
if [ "$script" = "docker" ] || [ "$script" = "nerdctl" ]; then
    source $tools_location/run-container.sh $environment $command $*
elif [ "$script" = "deploy" ]; then
    source $tools_location/run-deploy.sh $environment $command $*
else
    source $tools_location/general-func.sh $*
fi

# $SHELL
