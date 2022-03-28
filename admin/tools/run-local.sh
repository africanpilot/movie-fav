#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# imports
location=admin/tools
source $location/general-func.sh

# check SERVICES_TODO env set
validate_service_todo_env

todo=${SERVICES_TODO}
environment="$1"
command="$2"
shift 2

if [ "$command" == "up" ]; then
    # start local dev
    if exists_in_list "$todo" " " "db/postgres"; then
        sed -i 's/postgres_genmsdbtest/postgres_secmsdb/' "db/postgres/docker-compose.yml"
        gnome-terminal --tab --title="Local Postgres" --command="bash -c 'export $(grep -v '^#' .env | xargs); docker-compose -f db/postgres/docker-compose.yml -p services up; $SHELL'"
    fi

    if exists_in_list "$todo" " " "db/redis"; then
        sed -i 's/redis_genmsdbtest/redis_secmsdb/' "db/redis/docker-compose.yml"
        gnome-terminal --tab --title="Local Redis" --command="bash -c 'export $(grep -v '^#' .env | xargs); docker-compose -f db/redis/docker-compose.yml -p services up; $SHELL'"
    fi

    # update docker-compose file for correct volume
    if [ "$environment" == "test" ]; then
        sed -i 's/postgres_secmsdb/postgres_genmsdbtest/' "db/postgres/docker-compose.yml"
        sed -i 's/redis_secmsdb/redis_genmsdbtest/' "db/redis/docker-compose.yml"
        gnome-terminal --tab --title="Local test" --command="bash -c 'export $(grep -v '^#' .env | xargs); $SHELL'"
    else
        # start services...need a more clever way
        for d in $todo; do
            sed -i '/APP_DEFULT_ENV/c\APP_DEFULT_ENV=local' $d/.env
        done

        if exists_in_list "$todo" " " "server"; then
            gnome-terminal --tab --title="Local account" --command="bash -c 'export $(grep -v '^#' .env | xargs); python3 ./server/start account; $SHELL'"
            gnome-terminal --tab --title="Local movie" --command="bash -c 'export $(grep -v '^#' .env | xargs); python3 ./server/start movie; $SHELL'"
        fi

        # sleep then start apollo
        if exists_in_list "$todo" " " "api/apollo"; then
            echo "Waiting for all services to start. Sleepiong 15 seconds..."
            sleep 15
            gnome-terminal --tab --title="Local Apollo" --command="bash -c 'export $(grep -v '^#' .env | xargs); npm --prefix api/apollo run start-gateway; $SHELL'"
        fi

        if exists_in_list "$todo" " " "client"; then
            gnome-terminal --tab --title="Local Client" --command="bash -c 'export $(grep -v '^#' .env | xargs); npm --prefix client run start; $SHELL'"
        fi

    fi
elif [ "$command" == "build" ]; then

    if exists_in_list "$todo" " " "db/postgres"; then
        docker-compose -f db/postgres/docker-compose.yml -p services build
    fi

    if exists_in_list "$todo" " " "db/redis"; then
        docker-compose -f db/redis/docker-compose.yml -p services build
    fi

elif [ "$command" == "down" ]; then

    if exists_in_list "$todo" " " "db/postgres"; then
        docker-compose -f db/postgres/docker-compose.yml -p services down -v --remove-orphans
    fi

    if exists_in_list "$todo" " " "db/redis"; then
        docker-compose -f db/redis/docker-compose.yml -p services down -v --remove-orphans
    fi

    if [ "$environment" != "test" ]; then
        if exists_in_list "$todo" " " "server"; then
            pkill gunicorn
            echo "Gunicorn shutdown complete"
            kill -9 $(lsof -t -i:4001)
            kill -9 $(lsof -t -i:4002)
            echo "Uvicorn shutdown complete"
        fi

        if exists_in_list "$todo" " " "api/apollo"; then
            kill -9 $(lsof -t -i:4000)
            echo "Apollo server shutdown complete"
        fi
        
        if exists_in_list "$todo" " " "client"; then
            kill -9 $(lsof -t -i:3000)
            echo "Client server shutdown complete"
        fi
    fi
else
    echo "Known exception"
    return 1
fi

deactivate

echo "Done"
echo "******************************"
echo " "
