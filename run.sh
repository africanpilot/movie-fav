#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

todo="\
    db/postgres \
    db/redis \
    server \
    api/apollo \
    client \
    api/nginx
"

# db/postgres \
# db/redis \
# server \
# api/apollo \
# client \
# api/nginx \
# api/nginx-apollo \

export SERVICES_TODO="$todo"
location=admin/tools
script="$1"
environment="$2"
command="$3"
shift 2

case $script in
docker|local|deploy)
    a=1
    ;;
*)
    echo "Invalid script: $script"
    return 1
    ;;
esac

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

echo "script: $script"
echo "environment: $environment"
echo "command: $command"

# check for secrets file
if [ -f ".env" ]; then
    sed -i "/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=$environment" .env
    for d in $todo; do
        cp .env "$d"
    done
else
    echo "Please add and configure the .env file"
    return 1
fi

# sudo chmod -R 777 .  # might just direct to certbot

# redirect to script
if [ "$script" == "local" ]; then
    source $location/run-local.sh $environment $command
elif [ "$script" == "docker" ]; then
    source $location/run-docker.sh $environment $command
elif [ "$script" == "deploy" ]; then
    source $location/run-deploy.sh $environment $command
else
    echo "Unknown Exception met"
    return 1
fi