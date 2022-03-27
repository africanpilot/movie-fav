#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# run from root
if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

todo_tests="\
    account \
    movie
"
# account \
# movie

tools_location=admin/tools

echo " "
echo "******************************"
echo "STEP 1/2: Starting test enviornment"
echo "******************************"
echo " "

# set all env variables
export $(grep -v '^#' .env | xargs)

# install server requirments
source $tools_location/install-server-env.sh 

# install postgres requirements
source $tools_location/install-postgres-env.sh
sed -i 's/postgres_secmsdb/postgres_genmsdbtest/' "db/postgres/docker-compose.yml"

# install redis requirements
source $tools_location/install-redis-env.sh
sed -i 's/redis_secmsdb/redis_genmsdbtest/' "db/redis/docker-compose.yml"

# bring up postgres and redis dbs
docker-compose -f db/postgres/docker-compose.yml -p services up -d
docker-compose -f db/redis/docker-compose.yml -p services up -d

echo " "
echo "******************************"
echo "STEP 2/2: Running pytest: $todo_tests"
echo "******************************"
echo " "

echo "Sleeping 15 secs for db to start"

sleep 15

function clear_env
{
    echo " "
    echo "******************************"
    echo "Removing docker enviornments"
    echo "******************************"
    echo " "
    docker-compose -f db/postgres/docker-compose.yml -p services down -v --remove-orphans
    docker-compose -f db/redis/docker-compose.yml -p services down -v --remove-orphans
    deactivate
}

# Run pytests locally before pushing
for dotest in $todo_tests; do
    echo " "
    echo "******************************"
    echo "Entering: $dotest"
    echo "******************************"
    echo " "

    > "server/.pytest_cache/v/cache/lastfailed"
    pytest -x -v -m $dotest server/apps/$dotest

    # read results for any failures and exit if any
    test_result=$(jq . server/.pytest_cache/v/cache/lastfailed)
    if [[ ! -z $test_result ]]; then
        clear_env
        echo "WARNING: FAILED Server Tests. Please correct errors for server tests and rerun pipeline"
        return 1
    fi
done

clear_env

echo " "
echo "******************************"
echo "Done run-test-server.sh"
echo "******************************"
echo " "