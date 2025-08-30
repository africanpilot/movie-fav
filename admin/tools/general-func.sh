#!/bin/bash

validate_engine () {
    if [ "$1" = "docker" ]; then
        if command -v docker &> /dev/null; then
            DOCKER="docker"
            DOCKER_COMPOSE="docker compose"
            APP_DEFAULT_ENV="DEFAULT"
            announce "WARNING: Docker engine depricated Use lima script instead"
        else
            echo "CRITICAL ERROR: docker does not exist or please start the docker engine"
            return 1
        fi
    fi

    if [ "$1" = "nerdctl" ]; then
        if command -v nerdctl &> /dev/null; then
            DOCKER="nerdctl"
            DOCKER_COMPOSE="nerdctl compose"
        else
            echo "CRITICAL ERROR: nerdctl does not exist"
            return 1
        fi
    fi
}

create_env_from_sample () {
    environment="$1"
    if [ ! -f ".$environment.env" ]; then
        cp Sample-env .$environment.env
    fi
}

validate_script_agr () {
    case $1 in
    docker|nerdctl|deploy)
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
    dev|test|prod)
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
    build|up|down|pull|dry)
        a=1
        ;;
    *)
        echo "Invalid command: $1"
        return 1
        ;;
    esac
}

exists_in_list () {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    echo $LIST | tr "$DELIMITER" '\n' | grep -F -q -x "$VALUE"
}


get_list_of_services (){
    $(grep container_name: docker-compose-dev.yml | awk '{ printf $2 "," }')
}


validate_service_todo_env () {
    echo "checking validate_service_todo_env: ${SERVICES_TODO}"
    if [ -z "$SERVICES_TODO" ]; then
        services=$(grep container_name: docker-compose-dev.yml | awk '{ printf $2 "," }')
        export SERVICES_TODO=$services
        echo "SER: $SERVICES_TODO"
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
    d="$2"
    shift 2
    # xcommand="${ycommand} -p services down $d -v ${ORPHANS}"
    xcommand="${ycommand} -p services down"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_down"
	    return 1
    fi
}


docker_compose_build () {

    ycommand="$1"
    d="$2"
    shift 2
    xcommand="${ycommand} -p services build $d"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_build"
	    return 1
    fi
}


docker_compose_up () {

    ycommand="$1"
    d="$2"
    shift 2
    xcommand="${ycommand} -p services up -d $d"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_up"
	    return 1
    fi
}


docker_compose_pull () {

    ycommand="$1"
    d="$2"
    shift 2
    xcommand="${ycommand} -p services pull $d"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: docker_compose_pull"
	    return 1
    fi
}

nerdctl_build () {
    ycommand="$1"
    d="$2"
    shift 2
    xcommand="${ycommand} --build-arg APP_DEFAULT_ENV=${APP_DEFAULT_ENV} -t $d:${APP_DEFAULT_ENV} $*"
    announce "Running $xcommand"
    eval $xcommand
    if [ $? -ne 0 ]; then
        echo " CRITICAL ERROR: nerdctl_build"
	    return 1
    fi
}

helm_check () {
    chart=$1
    command=$2
    
    helm lint ./deployment/helm/$chart/
    helm install --dry-run --debug ./deployment/helm/$chart/ --generate-name
}

do_helm_deployment () {
    announce "Deploying $d"
    chart=$1
    command=$2

    helm upgrade -i --timeout 20s $chart ./deployment/helm/$chart/
}

do_dir () {
    d="$1"
    command="$2"
    shift 2
    case $command in
	build)
        # nerdctl build --namespace k8s.io -t $d ./microservices/.
        if [ "${DOCKER}" = "nerdctl" ]; then
            nerdctl_build "nerdctl build" $d ./microservices/.
        else
	        docker_compose_build "docker compose -f ${DOCKER_COMPOSE_FILE_NAME}" $d $*
	    fi
        ;;
     pull)
	    docker_compose_pull "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" $d $*
	    ;;
	 up)
	     docker_compose_up "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" $d $*
      	    ;;
	 down)
      	     docker_compose_down "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" $d $*
      	     ;;
       	 *)
	     echo " CRITICAL ERROR: Unknown command $1"
	     return 1
       	     ;;
	esac
}


announce_setup_check (){

    echo "******************************"
    echo "** $1"
    echo "******************************"
}


export_env_var () {
    environment=$1
    export $(grep -v '^#' .$environment.env | xargs)
}


validate_packages() {
    package_name=$1
    $package_name --version 2>&1 >/dev/null
    PACKAGE_IS_AVAILABLE=$?
    if [ $PACKAGE_IS_AVAILABLE -eq 0 ]; then
        echo "$package_name is installed"
    else
        echo "$package_name is not installed!"
    fi
}


validate_app_setup () {
    environment=$1
    echo " "
    echo "******************************"
    echo "Checking app integrity"
    echo "******************************"
    echo " "

    dir_todo="\
        microservices \
        microservices/apps/postgres \
        microservices/apps/rabbitmq \
        microservices/apps/redis
    "
    for d in $dir_todo; do
        if [ ! -d "$d" ]; then
            echo "CRITICAL ERROR: Please add the directory $d"
            return 1
        fi
    done

    if ! [ -x "$(command -v docker compose)" ]; then
        echo 'CRITICAL ERROR: docker compose is not installed.' >&2
        return 1
    fi

    create_env_from_sample $environment
    export_env_var $environment
}
