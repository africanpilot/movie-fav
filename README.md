## Commands

| Objective        | Command                                               |
| ---------------- | ----------------------------------------------------- |
| Help             | `./run.sh help` or `./run.sh -h` or `./run.sh --help` |
| General          | `./run.sh [script] [environment] [command] [target]`  |
| Dev Server       | `./run.sh docker dev up`                              |
| Prod Server      | `./run.sh docker prod up`                             |
| Test Server      | `./run.sh docker test up`                             |
| Specific Service | `./run.sh docker dev up movie`                        |
| Dry Run          | `./run.sh docker dev dry`                             |
| Helm Deployment  | `./run.sh deploy prod up`                             |
| Helm Dry Run     | `./run.sh deploy dev dry`                             |

## Installation

### Prerequisites

- **Docker**: This repo uses a Docker workflow for development, running tests, and simulating production environments
- **Docker Desktop**: Recommended for easy container management, viewing server logs, and other useful Docker features
- **Helm**: Required for Kubernetes deployments (if using deploy commands)

### Setup Steps

1. **Environment Configuration**:
   - Copy `sample-env` to `.dev.env`, `.test.env`, or `.prod.env` as needed
   - Edit the environment files with your specific configuration values

2. **Service Selection**:
   - Use the `SERVICES_TODO` variable in your `.env` file to specify which services to run
   - Alternatively, pass the service name as the fourth argument: `./run.sh docker dev up movie`

3. **Dependency Management**:
   - The script will automatically create environment files from the sample if they don't exist
   - Docker bind mounts connect the local codebase to containers for development hot-reloading

## pre-commit

- Install: https://pre-commit.com/
- running locally: This will also happen automatically before committing to a branch, but you can also run the tasks with `pre-commit run --all-files`

## Run Options

| Objective   | Command Options                      |
| ----------- | ------------------------------------ |
| script      | `docker`, `deploy`                   |
| environment | `dev`, `test`, `prod`                |
| command     | `build`, `up`, `down`, `pull`, `dry` |

## Script Types

- **docker**: Run Docker Compose operations for containerized services
- **deploy**: Run Helm deployments for Kubernetes

## Environment Types

- **dev**: Development environment with debug settings and hot reloading
- **test**: Testing environment for running automated tests
- **prod**: Production environment with optimized settings

## Commands

- **build**: Build Docker images for services
- **up**: Start services (runs in detached mode by default)
- **down**: Stop and remove running services
- **pull**: Pull latest Docker images from registry
- **dry**: Show what would be executed without actually running commands

## Features

### Help System

- Run `./run.sh help`, `./run.sh -h`, or `./run.sh --help` for usage information
- Improved error messages with helpful suggestions

### Service Targeting

- Target specific services: `./run.sh docker dev up movie`
- Use the `SERVICES_TODO` environment variable to specify which services to operate on

### Enhanced Error Handling

- Strict error checking with `set -euo pipefail`
- Descriptive error messages with suggested fixes
- Proper exit codes for scripting integration

### Dry Run Support

- Use `dry` command to see what would be executed without running
- Works for both Docker and Helm operations

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
