#!/bin/bash

set -e

# imports
location=admin/tools
source $location/general-func.sh

validate_service_todo_env

# init
PROJECT_OPTION=""
ORPHANS="--remove-orphans"


function do_subdirs
{
    topdir="$1"
    command="$2"
    shift 2

    for d in $(echo ${SERVICES_TODO} | sed "s/,/ /g"); do
        announce "ENTERING $d"

        # check docker file exsit before running commands
        if [ -f "${DOCKER_COMPOSE_FILE_NAME}" ]; then
            do_dir "$d" "$command" $*
        else
            echo "Did not find any expected Docker files in $d"
            return 1
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
