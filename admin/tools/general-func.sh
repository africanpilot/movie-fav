#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

validate_script_agr () {
    case $1 in
    docker|local|deploy|pipeline)
        a=1
        ;;
    *)
        echo "Invalid script: $1"
        return 1
        ;;
    esac
}

validate_enviornment_agr () {
    case $1 in
    test|prod|dev)
        a=1
        ;;
    *)
        echo "Invalid environment: $1"
        return 1
        ;;
    esac
}

validate_command_agr () {
    case $1 in
    build|up|down)
        a=1
        ;;
    *)
        echo "Invalid command: $1"
        return 1
        ;;
    esac
}

validate_app_setup () {
    echo " "
    echo "******************************"
    echo "Checking app integerity"
    echo "******************************"
    echo " "

    dir_todo="\
        db/postgres \
        db/redis \
        server \
        api/apollo \
        client \
        api/nginx \
        api/nginx-apollo \
    "
    for d in $dir_todo; do
        if [ ! -d "$d" ]; then
            echo "CRITICAL ERROR: Please add the directory $d"
            return 1
        fi
    done

    if [ ! -f ".env" ]; then
        echo "CRITICAL ERROR: Please add and configure the .env file"
        return 1
    fi

    if ! [ -x "$(command -v docker-compose)" ]; then
        echo 'CRITICAL ERROR: docker-compose is not installed.' >&2
        return 1
    fi
}

exists_in_list () {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    echo $LIST | tr "$DELIMITER" '\n' | grep -F -q -x "$VALUE"
}

pass_down_env_copies () {

    dir_todo="\
        db/postgres \
        db/redis \
        server \
        api/apollo \
        client \
        api/nginx \
        api/nginx-apollo \
    "

    for d in $dir_todo; do
        cp .env "$d"
    done
}

aws_erc_login () {
    aws ecr get-login-password --region $2 --profile default | docker login --username AWS --password-stdin $1.dkr.ecr.$2.amazonaws.com
}

validate_service_todo_env () {

    if set|grep '^SERVICES_TODO=' >/dev/null; then
        return
    else
    echo "CRITICAL ERROR: Please set and export the SERVICES_TODO env"
        return 1
    fi
}

set_environment () {

    APP_DEFAULT_ENV=$1
    if [ "test" == "$1" ] || [ "dev" == "$1" ]; then
        not_in_prod=1
        PROJECT_OPTION=" -p services "
    fi
}

# Just print a headline type message
announce (){

    echo "******************************"
    echo "** ${APP_DEFAULT_ENV} / " $*
    echo "******************************"
}

docker_compose_down () {

    ycommand="$1"
    shift 1
    xcommand="${ycommand} -p services down -v ${ORPHANS}"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_down"
	    return 1
    fi
}

docker_compose_build () {

    echo $*
    ycommand="$1"
    shift 1
    xcommand="${ycommand} build $*"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_build"
	    return 1
    fi
}

docker_compose_up () {

    ycommand="$1"
    shift 1
    xcommand="${ycommand} ${PROJECT_OPTION}up -d $*"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_up"
	    return 1
    fi
}

do_dir () {

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
	     echo " CRITICAL ERROR: Unknown command $1"
	     return 1
       	     ;;	
	esac
}

do_custom () {

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

install_server_env () {

    echo " "
    echo "******************************"
    echo "Setting up server dependancies"
    echo "******************************"
    echo " "

    if [ -d "server/pyenv" ] 
    then
        echo "Directory server/pyenv exists."
        source server/pyenv/bin/activate
    else
        echo "Directory server/pyenv does not exists. Installing Enviornment"
        python3.10 -m venv server/pyenv
        source server/pyenv/bin/activate
        pip install -r server/requirements.txt
    fi
}

install_api_env () {

    echo " "
    echo "******************************"
    echo "Setting up apollo packages"
    echo "******************************"
    echo " "

    if [ -d "api/apollo/node_modules" ] 
    then
        echo "Directory api/apollo/node_modules exists."
    else
        echo "Directory api/apollo/node_modules does not exists. Installing Enviornment"
        npm --prefix api/apollo install
    fi
}

install_client_env () {

    echo " "
    echo "******************************"
    echo "Setting up client packages"
    echo "******************************"
    echo " "

    if [ -d "client/node_modules" ] 
    then
        echo "Directory client/node_modules exists."
    else
        echo "Directory client/node_modules does not exists. Installing Enviornment"
        npm --prefix client install
    fi
}

validate_local_setup () {

    if exists_in_list "$1" " " "server"; then
        install_server_env
    fi
    if exists_in_list "$1" " " "client"; then
        install_client_env
    fi
    if exists_in_list "$1" " " "api/apollo"; then
        install_api_env
    fi
}

prep_for_deploy () {

    build_todo="\
        server \
        api/apollo \
        client \
        api/nginx-apollo
    "
    for d in $build_todo; do
        sed -i 's/# build: ./build: ./' "$d/docker-compose.yml"
        sed -i 's/build: ./# build: ./' "$d/docker-compose.yml"
    done
}

prep_for_dev () {

    build_todo="\
        server \
        api/apollo \
        client \
        api/nginx-apollo
    "
    for d in $build_todo; do
        sed -i 's/# build: ./build: ./' "$d/docker-compose.yml"
    done
}


# validate_orign_run_command
