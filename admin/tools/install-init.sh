#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.

set -e

echo " "
echo "******************************"
echo "STEP 1/5: Installing updates, upgrades and firewall rules"
echo "******************************"
echo " "
sudo apt-get update
sudo apt-get upgrade -y

sudo ufw status
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
sudo ufw status

# Install Docker: https://docs.docker.com/engine/install/ubuntu/
echo " "
echo "******************************"
echo "STEP 2/5: Setting up docker"
echo "******************************"
echo " "
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker-compose: https://docs.docker.com/compose/install/
echo " "
echo "******************************"
echo "STEP 3/5: Setting up docker compose"
echo "******************************"
echo " "
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# add doocker to group
echo " "
echo "******************************"
echo "STEP 4/5: Setting up docker groups"
echo "******************************"
echo " "
sudo usermod -aG docker $USER
sudo systemctl daemon-reload
sudo systemctl restart docker

# clone repo
echo " "
echo "******************************"
echo "STEP 5/5: Setting up repo"
echo "******************************"
echo " "
git clone "https://username:password@github.com/username/repository.git" # make sure to configure this line
sudo chmod +rwx .env
sudo cp .env movie-fav/.env

cd movie-fav

echo " "
echo "******************************"
echo "done"
echo "******************************"
echo " "