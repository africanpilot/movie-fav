#!/bin/bash

set -euo pipefail

# imports
location=admin/tools
source $location/general-func.sh

validate_service_todo_env


function do_subdirs
{
    local topdir="$1"
    local command="$2"
    shift 2

    for d in $(echo ${SERVICES_TODO} | sed "s/,/ /g"); do
        announce "PROCESSING HELM CHART: $d"

        # check helm chart exists
        if [ ! -d "deployment/helm/$d" ]; then
            echo "CRITICAL ERROR: Please add the directory deployment/helm/$d" >&2
            return 1
        fi

        if [ "$command" = "dry" ]; then
            helm_check "$d" "$command" "$@"
        else
            do_helm_deployment "$d" "$command" "$@"
        fi
    done
}


function main
{
    if [ $# -lt 2 ]; then
        echo "ERROR: Insufficient arguments" >&2
        echo "Usage: $0 [ENVIRONMENT] [COMMAND] [ARGS...]" >&2
        echo "Example: $0 dev dry" >&2
        return 1
    fi

    local environment="$1"
    local command="$2"
    shift 2

    set_environment "$environment"

    do_subdirs "$(pwd)" "$command" "$@"
}

main "$@"
