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
PROJECT_OPTION=""
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

    # update .env file for match dev setting
    if [ "$d" == "server" ] && [ "$command" == "up" ] && [ "$environment" != "prod" ]
    then
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
    

	if [ -f "docker-compose.yml" ] || [ -f "Dockerfile" ]
	then
        
        # update docker-compose file for correct volume
        if [ "$d" == "db/postgres" ] || [ "$d" == "db/redis" ]; then
            if [ "$environment" == "test" ]; then
                sed -i 's/postgres_secmsdb/postgres_genmsdbtest/' "docker-compose.yml"
                sed -i 's/redis_secmsdb/redis_genmsdbtest/' "docker-compose.yml"   
            else
                sed -i 's/postgres_genmsdbtest/postgres_secmsdb/' "docker-compose.yml"
                sed -i 's/redis_genmsdbtest/redis_secmsdb/' "docker-compose.yml"
            fi
        fi

        if [ "$command" == "up" ]
        then
            if [ "$d" == "api/apollo" ] && [ "$command" == "up" ]
            then
                echo "Waiting for all services to start. Sleepiong 15 seconds..."
                sleep 15
            fi
            gnome-terminal --tab --title="Local dev $d" --command="bash -c 'export $(grep -v '^#' .env | xargs); docker-compose -p services "$command" $*; $SHELL'"
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
    if [ $# -lt 2 ]; then
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