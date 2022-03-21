#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

not_in_prod_todo="\
	db \
"
todo="\
	server \
    api/apollo \
    client \
"
##########

# START_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# echo "d=$START_DIR"
# cd $START_DIR
pwd

PROJECT_OPTION=""
not_in_prod=0

ORPHANS="--remove-orphans"
db_host="localhost"

# function project_root
# {
#     cd $START_DIR
# }


function set_todo
{
    if [ $not_in_prod -eq 1 ]
    then
	todo="$not_in_prod_todo $todo"
    fi
    echo "Todo list: $todo"
}
#
# MOVIE_FAV_ENV environment variable must be set to build|test|dev
#
function set_environment
{

    MOVIE_FAV_ENV=$1
    export MOVIE_FAV_ENV
    echo "Setting environment to $MOVIE_FAV_ENV"

    if [ "test" == "$MOVIE_FAV_ENV" ] || [ "dev" == "$MOVIE_FAV_ENV" ]
    then
	not_in_prod=1
	PROJECT_OPTION=" -p services "
    fi
    set_todo
}

#
# Just print a headline type message
#
function announce
{
    echo "******************************"
    echo "** $MOVIE_FAV_ENV / " $*
    echo "******************************"
    
}

#
# Generic build instructions
#

function docker_compose_down
{
    ycommand="$1"
    shift 1
    # xcommand="${ycommand} -p services down -v --rmi all ${ORPHANS}"
    xcommand="${ycommand} -p services down -v ${ORPHANS}"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]
    then
	return 1
    fi
#    ORPHANS=
}
function docker_compose_build
{
    echo $*
    ycommand="$1"
    shift 1
    xcommand="${ycommand} build $*"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]
    then
	return 1
    fi
}

function docker_compose_up
{
    ycommand="$1"
    shift 1
    xcommand="${ycommand} ${PROJECT_OPTION}up -d $*"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]
    then
	return 1
    fi
}

#
# Execute a test 
#
function docker_compose_test
{
    echo "boo"
 ##   docker-compose run $PROJECT_OPTION --rm -w workingdir app /foo/bin/testrunner
}

#
#
#

function do_dir
{
    d="$1"
    command="$2"
    echo "C=$command"
    shift 2
    case $command in
	build)
	    docker_compose_build "docker-compose" $*
	    ;;
	 up)
	     docker_compose_up "docker-compose" $*
      	    ;;
	 down)
      	     docker_compose_down "docker-compose" $*
      	     ;;
       	 *)
	     echo "Unknown command $1"
	     return 1
       	     ;;	
	esac
}

function do_custom
{
    d="$1"
    command="$2"
    shift 2
    case $command in
	build)
	    docker_compose_build "./custom-compose" $*
	    ;;
	 up)
	     docker_compose_up "./custom-compose" $*
      	    ;;
	 down)
      	     docker_compose_down "./custom-compose" $*
      	     ;;
       	 *)
	     echo "Unknown command $1"
	     return 1
       	     ;;	
	esac
}

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
    sed -i "/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=$environment" .env
    if [ "$d" == "server" ] && [ "$command" == "up" ] && [ "$environment" != "prod" ]
    then
        echo "Waiting for all database to start. Sleeping 15 seconds..."
        sleep 15

        # get ip address for docker postgres database
        db_address=$(docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -qf "name=psqldb_secmsdb"))
        strip_text="/psqldb_secmsdb - "
        db_ip_address_value="${db_address/$strip_text/""}"
        sed -i "/DB_LOCAL_HOST/c\DB_LOCAL_HOST=$db_ip_address_value" .env
    fi
    

	if [ -f "docker-compose.yml" ] || [ -f "Dockerfile" ]
	then
        
        # update docker-compose file for correct volume
        # if [ "$1" == "test" ]
        # then
        #     sed -i 's/postgres_secmsdb/postgres_genmsdbtest/' "docker-compose.yml"
        # else
        #     sed -i 's/postgres_genmsdbtest/postgres_secmsdb/' "docker-compose.yml"
        # fi

        if [ "$command" == "up" ]
        then
            if [ "$d" == "api/apollo" ] && [ "$command" == "up" ]
            then
                echo "Waiting for all services to start. Sleepiong 15 seconds..."
                sleep 15
            fi
            gnome-terminal --tab --title="Local dev $d" --command="bash -c 'source admin/tools/install.sh; docker-compose -p services "$command" $*; $SHELL'"
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

    case $environment in
	test|prod|dev)
	    a=1
	    ;;
	*)
	    echo "Invalid environment: $environment"
	    return 1
	    ;;
    esac

    case $command in
	build|up|down)
	    a=1
	    ;;
	*)
	    echo "Invalid command: $command"
	    return 1
	    ;;
    esac

    set_environment $environment
    
    do_subdirs `pwd` $command $*

    # need a way to close all other tabs except current one
    # if [ "$command" == "down" ]
    # then
    #     killall gnome-terminal
    # fi  
}
main $*
