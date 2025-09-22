#!/bin/bash

set -euo pipefail

# imports
location=admin/tools
source $location/general-func.sh

validate_service_todo_env

# init
PROJECT_OPTION=""
ORPHANS="--remove-orphans"


function do_subdirs
{
    local topdir="$1"
    local command="$2"
    shift 2

    for d in $(echo ${SERVICES_TODO} | sed "s/,/ /g"); do
        announce "PROCESSING SERVICE: $d"

        # check docker file exists before running commands
        if [ -f "${DOCKER_COMPOSE_FILE_NAME}" ]; then
            do_dir "$d" "$command" "$@"
        else
            echo "CRITICAL ERROR: Docker compose file not found: ${DOCKER_COMPOSE_FILE_NAME}" >&2
            return 1
        fi
    done
}


function main
{
    if [ $# -lt 2 ]; then
        echo "ERROR: Insufficient arguments" >&2
        echo "Usage: $0 [ENVIRONMENT] [COMMAND] [ARGS...]" >&2
        echo "Example: $0 dev up" >&2
        return 1
    fi

    local environment="$1"
    local command="$2"
    shift 2

    set_environment "$environment"

    do_subdirs "$(pwd)" "$command" "$@"
}

main "$@"
