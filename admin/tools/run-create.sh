#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

name="$1"
port="$2"
shift 2

# copy skeleton
cp -R server/apps/skeleton "server/apps/$name"

# add port to env file
env_file="server/.env"
if [ -f $env_file ]
then
    echo "" >> $env_file
    echo "APP_PORT_${name^^}=$port" >> $env_file
else
    echo "Did not find $env_file"
    return 1
fi

# add name and port info docker-compose.yml
compose_file="server/docker-compose.yml"
if [ -f $compose_file ]
then
    sed -i '/# LINE-REF-DONT-DELETE.*/r'<(
        echo "  $name:"
        echo "    image: $name:dev"
        echo "    hostname: $name"
        echo "    build: ."
        echo "    entrypoint: [/home/moviefav/server/start, $name]"
        echo "    labels:"
        echo "        - 'com.moviefav.description=$name'"
        echo "        - 'com.moviefav.server'"
        echo "        - 'kompose.service.type=nodeport'"
        echo "    restart: 'on-failure'"
        echo "    env_file:"
        echo "        - .env"
        echo "    ports:"
        echo "        - '$port:$port'"
        echo "    networks:"
        echo "        - secmsapp"
        echo "        - secmsdbs"
        echo "        - mstoapi"
        echo ""
    ) -- $compose_file
    sed -i '/# LINE-REF-DONT-DELETE/c\' $compose_file
    sed -i '/# CONST-REF-DONT-DELETE/c\# LINE-REF-DONT-DELETE\n# CONST-REF-DONT-DELETE' $compose_file
else
    echo "Did not find $compose_file"
    return 1
fi