#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

# imports
tools_location=admin/tools
source $tools_location/general-func.sh

todo="\
    server \
    api/apollo \
    client \
    api/nginx-apollo \
    api/nginx-certbot-init
"

# server \
# api/apollo \
# client \
# api/nginx-apollo


if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
    return 1
fi

if [ ! -f ".env" ]; then
    echo "Please add and configure the .env file"
    return 1
fi


echo " "
echo "******************************"
echo "STEP 1/5: Setting enviornment varables"
echo "******************************"
echo " "

export $(grep -v '^#' .env | xargs)

echo " "
echo "******************************"
echo "STEP 2/2: Push todo to aws erc: $todo"
echo "******************************"
echo " "

for d in $todo; do
    echo "******************************"
    echo "** Adding: $d"
    echo "******************************"
    
    location=$d
    
    if [ "$d" == "server" ]; then
        AWS_REPO_NAME="server"
    elif [ "$d" == "api/apollo" ]; then
        AWS_REPO_NAME="apollo"
    elif [ "$d" == "client" ]; then
        AWS_REPO_NAME="client"
    elif [ "$d" == "api/nginx-certbot-init" ]; then
        AWS_REPO_NAME="nginx-certbot-init"
        location="api/nginx-apollo"
        
        # replace docker file
        > "api/nginx-apollo/Dockerfile"

        echo 'FROM nginx:stable-alpine

        COPY conf/nginx-certbot-init.conf /etc/nginx/nginx-certbot-init.conf
        COPY conf/default.conf /etc/nginx/conf.d/

        ENTRYPOINT ["nginx", "-g", "daemon off;"]
        ' >> "api/nginx-apollo/Dockerfile"

    elif [ "$d" == "api/nginx-apollo" ]; then
        AWS_REPO_NAME="nginx-apollo"

        # replace docker file
        > "api/nginx-apollo/Dockerfile"

        echo 'FROM nginx:stable-alpine

        COPY conf/nginx.conf /etc/nginx/nginx.conf
        COPY conf/default.conf /etc/nginx/conf.d/

        ENTRYPOINT ["nginx", "-g", "daemon off;"]
        ' >> "api/nginx-apollo/Dockerfile"
    elif [ "$d" == "api/nginx" ]; then
        AWS_REPO_NAME="nginx"
    else
        echo "Please use an exsiting directory or add a new one"
        return 1
    fi
    echo "AWS_REPO_NAME: $AWS_REPO_NAME" 
    aws ecr describe-repositories --repository-names $AWS_REPO_NAME || aws ecr create-repository --repository-name $AWS_REPO_NAME --profile default --region ${AWS_REGION}
    aws_erc_login ${AWS_ACCOUNT_ID} ${AWS_REGION}
    docker buildx build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$AWS_REPO_NAME:latest --push $location
done

echo " "
echo "******************************"
echo "Done"
echo "******************************"
echo " "