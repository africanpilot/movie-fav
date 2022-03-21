- all database will always be docker to keep setup simple

pre-requirements: linux env
    A) local dev:

        1) python3 and venv
            
            Install python version:
            1) sudo apt update 
            2) sudo apt-get install python
                **Note: (you can specify version example: sudo apt-get install python3.7)


            Install Env: https://linoxide.com/how-to-create-python-virtual-environment-on-ubuntu-20-04/
            1) sudo apt update
            2) sudo apt install python3-pip
            3) sudo apt-get install python3-venv

        2) node: **must upgrade to version 17 or greater

            Install node: https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04
            1) sudo apt update
            2) cd ~
            3) curl -sL https://deb.nodesource.com/setup_17.x -o nodesource_setup.sh
            4) sudo bash nodesource_setup.sh
            5) sudo apt install nodejs -y
            
    B) Docker dev:

        1) linux env
        2) docker and docker compose

            Install Docker: https://docs.docker.com/engine/install/ubuntu/
            1) sudo apt-get update
            2) curl -fsSL https://get.docker.com -o get-docker.sh
            3) sudo sh get-docker.sh

            Install Docker-compose: https://docs.docker.com/compose/install/
            1) sudo apt-get update
            2) sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            3) sudo chmod +x /usr/local/bin/docker-compose


Main commands: always from root project folder

local dev mode:

    ```bash
        source run-local-dev.sh dev up
        source run-local-dev.sh dev down
    ```

local test mode:
    ```bash
        source run-local-dev.sh test up
        source run-local-dev.sh test down
        pytest -v -m account server/apps/account
        pytest -v -m movie server/apps/movie
        pytest -v -m account_bench server/apps/account
        pytest -v -m movie_bench server/apps/movie
    ```

docker dev mode:

    ```bash
        source run-docker-dev.sh dev build
        source run-docker-dev.sh dev up
        source run-docker-dev.sh dev down
    ```
- After bring the service down, you can use ctrl + d to close out of old tabs in the terminal

-------------------------Other Useful commands---------------------------------------------------------------
starting single app
```bash
    python3 ./server/start movie
```

start apollo
```node
    npm --prefix api/apollo run start-gateway
```

start client
```node
    npm run start
```

Docker methods

ALL
- docker-compose -f db/docker-compose.yml -p services build; docker-compose -f db/docker-compose.yml -p services up

- docker-compose -f server/docker-compose.yml -p services build; docker-compose -f server/docker-compose.yml -p services up

- docker-compose -f api/apollo/docker-compose.yml -p services build; docker-compose -f api/apollo/docker-compose.yml -p services up

JUST ONE
- docker-compose -p services build psqldb_secmsdb; docker-compose -p services up psqldb_secmsdb
- docker-compose -p services build movie; docker-compose -p services up movie

Get IP Address
- docker ps
- docker inspect $(docker ps -qf "name=psqldb_secmsdb") | grep IPAddress
- docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -qf "name=psqldb_secmsdb")


-------