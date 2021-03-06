#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# imports
location=admin/tools
source $location/general-func.sh

# check SERVICES_TODO env set
validate_service_todo_env

# init
todo=${SERVICES_TODO}
PROJECT_OPTION=" -p services "
not_in_prod=0
not_in_prod_todo=""
ORPHANS="--remove-orphans"
db_host="localhost"


function do_subdirs
{
    topdir="$1"
    command="$2"
    shift 2
    for d in $todo; do
	echo "CCCC=$@"
	announce "ENTERING $d"
	cd $d

	if [ -f "docker-compose.yml" ] || [ -f "Dockerfile" ]
	then
        # extra conditions for db dir
        if [ "$d" == "db/postgres" ] || [ "$d" == "db/redis" ]; then
            # update docker-compose file for correct volume
            sed -i 's/postgres_genmsdbtest/postgres_secmsdb/' "docker-compose.yml"
            sed -i 's/redis_genmsdbtest/redis_secmsdb/' "docker-compose.yml"
        fi
        
        if [ "$command" == "up" ]
        then
            
            # extra conditions for server dir
            if [ "$d" == "server" ]; then
                echo "Waiting for all database to start. Sleeping 15 seconds..."
                sleep 15

                # get ip address for docker postgres database
                db_address=$(docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -qf "name=psqldb_secmsdb"))
                strip_text="/psqldb_secmsdb - "
                db_ip_address_value="${db_address/$strip_text/""}"
                sed -i "/DB_LOCAL_HOST/c\DB_LOCAL_HOST=$db_ip_address_value" .env

                # get ip address for docker redis database
                db_address=$(docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -qf "name=redisdb_secmsdb"))
                strip_text="/redisdb_secmsdb - "
                db_ip_address_value="${db_address/$strip_text/""}"
                sed -i "/DB_REDIS_HOST/c\DB_REDIS_HOST=$db_ip_address_value" .env
            fi

            # extra conditions for apollo dir
            if [ "$d" == "api/apollo" ]; then
                echo "Waiting for all services to start. Sleeping 15 seconds..."
                sleep 15
            fi

            # extra conditions for apollo dir
            if [ "$d" == "api/nginx" ]; then
                echo "Waiting for apollo to start. Sleeping 15 seconds..."
                sleep 15
            fi

            # finally execute docker compose commands
            do_dir "$d" "$command" $*
        else
            do_dir "$d" "$command" $*
        fi     
	else
	    echo "Did not find any expected Docker files in $d"
	    return 1
	fi
	cd $topdir
    done
}

function main
{
    top_dirs=`ls -d */| tr -d "/"`
    if [ $# -lt 2 ]
    then
	top_dirs=`echo -n "$top_dirs" | tr "\n" "|"`
	echo "Use $0 [ENVIRONMENT] [COMMAND] [COMPOSER  ARGS:args..]"
	return 1
    fi

    environment="$1"
    command="$2"
    shift 2

    set_environment $environment

    do_subdirs `pwd` $command $*
 
}
main $*