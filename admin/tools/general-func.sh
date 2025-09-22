#!/bin/bash

# Set strict error handling
set -euo pipefail

# Display help information
show_help() {
    cat << EOF
Movie-Fav Management Scripts

USAGE:
    ./run.sh [SCRIPT] [ENVIRONMENT] [COMMAND] [TARGET]

ARGUMENTS:
    SCRIPT      - Type of script to run (docker, deploy)
    ENVIRONMENT - Target environment (dev, test, prod)
    COMMAND     - Action to perform (build, up, down, pull, dry)
    TARGET      - Optional: Specific service to target

EXAMPLES:
    ./run.sh docker dev up           # Start dev environment
    ./run.sh docker prod build      # Build prod services
    ./run.sh deploy dev dry          # Dry run deployment
    ./run.sh docker dev up movie     # Start only movie service

COMMANDS:
    build  - Build Docker images
    up     - Start services (detached by default)
    down   - Stop and remove services
    pull   - Pull latest images
    dry    - Show what would be executed without running

ENVIRONMENTS:
    dev    - Development environment
    test   - Testing environment
    prod   - Production environment

For more information, see the README.md file.
EOF
}

validate_engine () {
    local engine="$1"
    if [ "$engine" = "docker" ]; then
        if command -v docker &> /dev/null; then
            DOCKER="docker"
            DOCKER_COMPOSE="docker compose"
            APP_DEFAULT_ENV="DEFAULT"
        else
            echo "CRITICAL ERROR: Docker is not installed or Docker engine is not running" >&2
            echo "Please install Docker and ensure the Docker engine is started" >&2
            return 1
        fi
    else
        echo "CRITICAL ERROR: Unsupported engine: $engine" >&2
        return 1
    fi
}

create_env_from_sample () {
    local environment="$1"
    local env_file=".${environment}.env"
    local sample_file="sample-env"

    if [ ! -f "$env_file" ]; then
        if [ -f "$sample_file" ]; then
            cp "$sample_file" "$env_file"
            echo "Created $env_file from $sample_file"
        else
            echo "CRITICAL ERROR: Sample environment file '$sample_file' not found" >&2
            return 1
        fi
    fi
}

validate_script_arg () {
    local script="$1"
    case $script in
    docker|deploy)
        return 0
        ;;
    *)
        echo "CRITICAL ERROR: Invalid script: $script" >&2
        echo "Valid scripts: docker, deploy" >&2
        return 1
        ;;
    esac
}


validate_environment_arg () {
    local environment="$1"
    case $environment in
    dev|test|prod)
        return 0
        ;;
    *)
        echo "CRITICAL ERROR: Invalid environment: $environment" >&2
        echo "Valid environments: dev, test, prod" >&2
        return 1
        ;;
    esac
}


validate_command_arg () {
    local command="$1"
    case $command in
    build|up|down|pull|dry)
        return 0
        ;;
    *)
        echo "CRITICAL ERROR: Invalid command: $command" >&2
        echo "Valid commands: build, up, down, pull, dry" >&2
        return 1
        ;;
    esac
}


validate_service_todo_env () {
    echo "checking validate_service_todo_env: ${SERVICES_TODO}"
    if [ -z "$SERVICES_TODO" ]; then
        services=$(grep container_name: docker-compose-dev.yml | awk '{ printf $2 "," }')
        export SERVICES_TODO=$services
        echo "SER: $SERVICES_TODO"
    fi
}


set_environment () {
    APP_DEFAULT_ENV=$1
    if [ "test" == "$1" ] || [ "dev" == "$1" ]; then
        not_in_prod=1
        PROJECT_OPTION=" -p services "
    fi
}

# Just print a headline type message
announce (){
    echo "******************************"
    echo "** ${APP_DEFAULT_ENV} / " $*
    echo "******************************"
}


docker_compose_down () {
    local compose_cmd="$1"
    local services="$2"
    shift 2

    local full_cmd="${compose_cmd} -p services down"
    announce "Running: $full_cmd"

    if ! eval "$full_cmd"; then
        echo "CRITICAL ERROR: Failed to bring down services" >&2
        echo "Command: $full_cmd" >&2
        return 1
    fi
}


docker_compose_build () {
    local compose_cmd="$1"
    local services="$2"
    shift 2

    local full_cmd="${compose_cmd} -p services build $services"
    announce "Running: $full_cmd"

    if ! eval "$full_cmd"; then
        echo "CRITICAL ERROR: Failed to build services" >&2
        echo "Command: $full_cmd" >&2
        return 1
    fi
}


docker_compose_up () {
    local compose_cmd="$1"
    local services="$2"
    shift 2

    local CICD_MODE=${CICD_MODE:-False}
    local detach_flag=""

    if [ "$CICD_MODE" != "True" ]; then
        detach_flag="-d"
    fi

    local full_cmd="${compose_cmd} -p services up $detach_flag $services"
    announce "Running: $full_cmd"

    if ! eval "$full_cmd"; then
        echo "CRITICAL ERROR: Failed to start services" >&2
        echo "Command: $full_cmd" >&2
        return 1
    fi
}


docker_compose_pull () {
    local compose_cmd="$1"
    local services="$2"
    shift 2

    local full_cmd="${compose_cmd} -p services pull $services"
    announce "Running: $full_cmd"

    if ! eval "$full_cmd"; then
        echo "CRITICAL ERROR: Failed to pull services" >&2
        echo "Command: $full_cmd" >&2
        return 1
    fi
}


helm_check () {
    local chart="$1"
    local command="$2"
    local chart_path="./deployment/helm/$chart/"

    if [ ! -d "$chart_path" ]; then
        echo "CRITICAL ERROR: Helm chart directory not found: $chart_path" >&2
        return 1
    fi

    announce "Validating Helm chart: $chart"

    if ! helm lint "$chart_path"; then
        echo "CRITICAL ERROR: Helm lint failed for chart: $chart" >&2
        return 1
    fi

    if ! helm install --dry-run --debug "$chart_path" --generate-name; then
        echo "CRITICAL ERROR: Helm dry-run failed for chart: $chart" >&2
        return 1
    fi

    echo "Helm chart validation successful for: $chart"
}


do_helm_deployment () {
    local chart="$1"
    local command="$2"
    local chart_path="./deployment/helm/$chart/"

    if [ ! -d "$chart_path" ]; then
        echo "CRITICAL ERROR: Helm chart directory not found: $chart_path" >&2
        return 1
    fi

    announce "Deploying Helm chart: $chart"

    if ! helm upgrade -i --timeout 20s "$chart" "$chart_path"; then
        echo "CRITICAL ERROR: Helm deployment failed for chart: $chart" >&2
        return 1
    fi

    echo "Helm deployment successful for: $chart"
}

do_dir () {
    local services="$1"
    local command="$2"
    shift 2

    case $command in
        build)
            docker_compose_build "docker compose -f ${DOCKER_COMPOSE_FILE_NAME}" "$services" "$@"
            ;;
        pull)
            docker_compose_pull "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" "$services" "$@"
            ;;
        up)
            docker_compose_up "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" "$services" "$@"
            ;;
        down)
            docker_compose_down "${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_FILE_NAME}" "$services" "$@"
            ;;
        dry)
            echo "DRY RUN: Would execute docker compose commands for services: $services"
            echo "Compose file: ${DOCKER_COMPOSE_FILE_NAME}"
            ;;
        *)
            echo "CRITICAL ERROR: Unknown command: $command" >&2
            echo "Valid commands: build, pull, up, down, dry" >&2
            return 1
            ;;
    esac
}


announce_setup_check (){
    echo "******************************"
    echo "** $1"
    echo "******************************"
}


export_env_var () {
    local environment="$1"
    local env_file=".${environment}.env"

    if [ ! -f "$env_file" ]; then
        echo "CRITICAL ERROR: Environment file not found: $env_file" >&2
        return 1
    fi

    # Export variables while ignoring comments and empty lines
    # Use grep and eval to handle special characters properly
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip empty lines and comments
        if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
            continue
        fi

        # Validate line format (KEY=VALUE)
        if [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
            # Remove surrounding quotes if they exist
            line=$(echo "$line" | sed "s/='\(.*\)'$/=\1/" | sed 's/="\(.*\)"$/=\1/')
            export "$line"
        fi
    done < "$env_file"

    echo "Loaded environment variables from: $env_file"
}


validate_packages() {
    package_name=$1
    $package_name --version 2>&1 >/dev/null
    PACKAGE_IS_AVAILABLE=$?
    if [ $PACKAGE_IS_AVAILABLE -eq 0 ]; then
        echo "$package_name is installed"
    else
        echo "$package_name is not installed!"
    fi
}


validate_app_setup () {
    environment=$1
    echo " "
    echo "******************************"
    echo "Checking app integrity"
    echo "******************************"
    echo " "
    # Check required directories
    required_dirs=(
        "microservices"
        "microservices/apps/postgres"
        "microservices/apps/rabbitmq"
        "microservices/apps/redis"
    )

    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            echo "CRITICAL ERROR: Please add the directory $dir"
            return 1
        fi
    done

    if ! [ -x "$(command -v docker compose)" ]; then
        echo 'CRITICAL ERROR: docker compose is not installed.' >&2
        return 1
    fi

    create_env_from_sample $environment
    export_env_var $environment
}
