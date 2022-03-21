#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.


location=admin/tools
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


if [ "$command" == "up" ]; then
    
    # start local dev
    gnome-terminal --tab --title="Local Database" --command="bash -c 'docker-compose -f db/docker-compose.yml -p services build; docker-compose -f db/docker-compose.yml -p services up; $SHELL'"
    
    # update docker-compose file for correct volume
    if [ "$environment" == "test" ]; then
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=test' server/.env
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=test' api/apollo/.env
        sed -i 's/postgres_secmsdb/postgres_genmsdbtest/' "db/docker-compose.yml"
        gnome-terminal --tab --title="Local test" --command="bash -c 'source admin/tools/install.sh; $SHELL'"
    else
        sed -i 's/postgres_genmsdbtest/postgres_secmsdb/' "db/docker-compose.yml"

        # start services...need a more clever way
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=local' server/.env
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=local' api/apollo/.env
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=local' client/.env
        sed -i '/MOVIE_FAV_ENV/c\MOVIE_FAV_ENV=local' api/nginx/.env
        gnome-terminal --tab --title="Local account" --command="bash -c 'source admin/tools/install.sh; python3 ./server/start account; $SHELL'"
        gnome-terminal --tab --title="Local movie" --command="bash -c 'source admin/tools/install.sh; python3 ./server/start movie; $SHELL'"

        # sleep then start apollo
        echo "Waiting for all services to start. Sleepiong 15 seconds..."
        sleep 15
        gnome-terminal --tab --title="Local Apollo" --command="bash -c 'source admin/tools/install.sh; npm --prefix api/apollo run start-gateway; $SHELL'"
        gnome-terminal --tab --title="Local Client" --command="bash -c 'source admin/tools/install.sh; npm --prefix client run start; $SHELL'"

    fi
elif [ "$command" == "build" ]; then
    source admin/tools/install.sh
    docker-compose -f db/docker-compose.yml -p services build
elif [ "$command" == "down" ]; then
    docker-compose -f db/docker-compose.yml -p services down -v --remove-orphans
    if [ "$environment" != "test" ]; then
        pkill gunicorn
        echo "Gunicorn shutdown complete"
        kill -9 $(lsof -t -i:4001)
        kill -9 $(lsof -t -i:4002)
        echo "Uvicorn shutdown complete"
        kill -9 $(lsof -t -i:4000)
        echo "Apollo server shutdown complete"
        kill -9 $(lsof -t -i:3000)
        echo "Client server shutdown complete"
    fi
else
    echo "Known exception"
    return 1
fi

echo "Done"
echo "******************************"
echo " "
