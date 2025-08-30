#!/bin/bash

set -e

# imports
location=admin/tools
source $location/general-func.sh

validate_service_todo_env


function do_subdirs
{
    topdir="$1"
    command="$2"
    shift 2

    for d in $(echo ${SERVICES_TODO} | sed "s/,/ /g"); do
        announce "ENTERING $d"

        # check helm chart exists
        if [ ! -d "deployment/helm/$d" ]; then
            echo "CRITICAL ERROR: Please add the directory depployment/helm/$d"
            return 1
        fi

        if [ "$command" = "dry" ]; then
            helm_check "$d" "$command" $*
        else
            do_helm_deployment "$d" "$command" $*
        fi
    done
}


function main
{
    top_dirs=`ls -d */| tr -d "/"`
    if [ $# -lt 2 ]; then
        top_dirs=`echo -n "$top_dirs" | tr "\n" "|"`
        echo "Use $0 [ENVIRONMENT] [COMMAND] [COMPOSER  ARGS:args..]"
	    return 1
    fi

    environment="$1"
    command="$2"
    shift 3

    set_environment $environment

    do_subdirs `pwd` $command $*

}
main $*
