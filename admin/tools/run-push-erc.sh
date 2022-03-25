#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.


todo="\
    api/nginx-apollo
"

# server \
# api/apollo \
# client \
# api/nginx-apollo

if [  ! -d "server" ]; then
    echo "You should only run this script from your application root directory"
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
    echo "** Entering: $d"
    echo "******************************"
    if [ "$d" == "server" ]; then
        AWS_REPO_NAME="server"
    elif [ "$d" == "api/apollo" ]; then
        AWS_REPO_NAME="apollo"
    elif [ "$d" == "client" ]; then
        AWS_REPO_NAME="client"
    elif [ "$d" == "api/nginx-apollo" ]; then
        AWS_REPO_NAME="nginx-apollo" #nginx-certbot-init
    elif [ "$d" == "api/nginx" ]; then
        AWS_REPO_NAME="nginx"
    else
        echo "Please use an exsiting directory or add a new one"
        return 1
    fi
    echo "AWS_REPO_NAME: $AWS_REPO_NAME" 
    aws ecr create-repository --repository-name $AWS_REPO_NAME --profile default --region ${AWS_REGION}
    aws ecr get-login-password --region ${AWS_REGION} --profile default | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
    docker buildx build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/$AWS_REPO_NAME:latest --push $d
done

echo " "
echo "******************************"
echo "Done"
echo "******************************"
echo " "
