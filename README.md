## Commands

| Objective      | Command
|----------------|-------------------------------------------------
| General        | `monxt [script] [environment] [command]`
| Dev Server     | `monxt docker dev up `
| Prod Server    | `monxt docker prod up`
| Test Server    | `monxt docker test up`


## Installation

- This repo uses a docker work flow for development, running tests, and simulating a prod environment. Bind mount will take care of connecting the microservices directory to the docker container to take advantage of the reloader when making changes locally. You can still, however, develop locally without docker on your own terms
- Install Docker Hub desktop: This is the best way to move through different containers, view server logs, and other useful docker features
- .env: Copy the "Sample-env" file and change it to ".env"
- specify ms: use the .env file var "SERVICES_TODO" when you want to specify the microservice to run.
- Homebrew: Install Homebrew. Other packages needed for the run.sh file will be installed using homebrew


## pre-commit

- Install: https://pre-commit.com/
- running locally: This will also happen automatically before committing to a branch, but you can also run the tasks with `pre-commit run --all-files`

## Run options


| Objective      | Command Options
|----------------|-------------------------------------------------
| script         | `docker`
| environment    | `dev, test, prod`
| command        | `build, up, down`


## Script

- currently only the docker script is available


## Environment

- There are 3 types of environments available dev, test, and prod. Each with there own docker compose file


## Command

- these commands are docker compose commands

## Directories

#### admin:
- here we can store general purpose scripts that will help with development. Documents for this repo will be stored here too

#### deployment
- placeholder for developing with deployment repos

#### microservices
- all core microservices go here.
- The use of the links directory allows us to have a space to share code between different microservices, thus reducing on duplicate code.
- This directory approach also focuses on providing standards, here the Dockerfile, makefile, start, and others apply to all microservices. However, one can still create a microservice with its own independent rules, but lets try not to do that.
- You are free to checkout other backend microservices that have not been officially migrated. There are some that have been tried and added to the docker-compose files.

## TODO
- should be all postgres dialect (from sqlalchemy import ...)
- change to movie_cast (person_cast: [String] @external)
- change ALL_MODELS to (ALL_DB_MODELS)
- ensure sitecustomize for links works and remove links files
- - fix grpc and fix it when in monxt mode