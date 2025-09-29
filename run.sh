#!/bin/bash

set -euo pipefail

# imports
tools_location=admin/tools
source $tools_location/general-func.sh

# Check for help flag or no arguments
if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    show_help
    exit 0
fi

# get args
script="$1"
environment="${2:-}"
command="${3:-}"
target="${4:-}"

# Validate minimum required arguments
if [ "$script" = "docker" ] || [ "$script" = "deploy" ]; then
    if [ -z "$environment" ] || [ -z "$command" ]; then
        echo "ERROR: Missing required arguments" >&2
        echo "Usage: $0 [SCRIPT] [ENVIRONMENT] [COMMAND] [TARGET]" >&2
        echo "Run '$0 help' for more information" >&2
        exit 1
    fi
fi

if [ -z "$script" ] || [ -z "$environment" ] || [ -z "$command" ]; then
    echo "ERROR: Missing required arguments" >&2
    echo "Usage: $0 [SCRIPT] [ENVIRONMENT] [COMMAND] [TARGET]" >&2
    echo "Run '$0 help' for more information" >&2
    exit 1
fi

# validation process
if [ "$script" = "docker" ] || [ "$script" = "deploy" ]; then
    shift 2
    validate_engine $script
    validate_script_arg $script
    validate_environment_arg $environment
    validate_command_arg $command
    validate_app_setup $environment
    # source .buildx.env

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
