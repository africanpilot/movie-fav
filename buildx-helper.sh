#!/bin/bash

# Docker Buildx Helper Script for movie-fav
# This script demonstrates different ways to use Docker Buildx with Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Docker Buildx Helper for movie-fav${NC}\n"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker Buildx is available
if ! docker buildx version >/dev/null 2>&1; then
    print_error "Docker Buildx is not available. Please install Docker Desktop or Docker CE with Buildx plugin."
    exit 1
fi

print_status "Docker Buildx is available"

# Create or use existing buildx builder
BUILDER_NAME="movie-fav-builder"

if ! docker buildx inspect $BUILDER_NAME >/dev/null 2>&1; then
    print_status "Creating new buildx builder: $BUILDER_NAME"
    docker buildx create --name $BUILDER_NAME --driver docker-container --use
    docker buildx inspect --bootstrap
else
    print_status "Using existing buildx builder: $BUILDER_NAME"
    docker buildx use $BUILDER_NAME
fi

# Function to build with cache
build_with_cache() {
    local service=$1
    local target=${2:-development}
    
    print_status "Building $service with buildx cache..."
    
    # Build with registry cache (requires pushing to registry)
    # docker buildx build \
    #   --target $target \
    #   --cache-from type=registry,ref=myregistry/movie-fav-cache:$service \
    #   --cache-to type=registry,ref=myregistry/movie-fav-cache:$service,mode=max \
    #   --load \
    #   -t $service:buildx \
    #   ./microservices
    
    # Build with local cache
    docker buildx build \
      --target $target \
      --cache-from type=local,src=/tmp/.buildx-cache-$service \
      --cache-to type=local,dest=/tmp/.buildx-cache-$service,mode=max \
      --load \
      -t $service:buildx \
      ./microservices
}

# Function to show usage
show_usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0 setup                    - Setup buildx builder"
    echo "  $0 build <service>          - Build service with cache"
    echo "  $0 build-all               - Build all services with cache"
    echo "  $0 compose-build           - Build using docker-compose with buildx"
    echo "  $0 compose-up              - Build and run using docker-compose with buildx"
    echo "  $0 clean-cache             - Clean buildx cache"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 build account           - Build account service"
    echo "  $0 compose-up              - Build and start all services"
    echo ""
    echo -e "${BLUE}Services:${NC} account, movie, person, shows, notifications, apollo, nginx, theater"
}

# Main script logic
case "${1:-}" in
    setup)
        print_status "Buildx builder setup complete!"
        ;;
    
    build)
        if [ -z "$2" ]; then
            print_error "Please specify a service to build"
            show_usage
            exit 1
        fi
        build_with_cache $2 development
        ;;
    
    build-all)
        print_status "Building all services with buildx cache..."
        services=("account" "movie" "person" "shows" "notifications")
        for service in "${services[@]}"; do
            build_with_cache $service development
        done
        build_with_cache "apollo" "apollo-production"
        build_with_cache "nginx" "nginx-production"
        build_with_cache "theater" "theater-production"
        print_status "All services built successfully!"
        ;;
    
    compose-build)
        print_status "Building with docker-compose and buildx..."
        export DOCKER_BUILDKIT=1
        export COMPOSE_DOCKER_CLI_BUILD=1
        docker-compose -f docker-compose-dev.yml build
        ;;
    
    compose-up)
        print_status "Building and starting services with docker-compose and buildx..."
        export DOCKER_BUILDKIT=1
        export COMPOSE_DOCKER_CLI_BUILD=1
        docker-compose -f docker-compose-dev.yml up --build -d
        ;;
    
    compose-buildx)
        print_status "Using optimized buildx compose file..."
        export DOCKER_BUILDKIT=1
        export COMPOSE_DOCKER_CLI_BUILD=1
        docker-compose -f docker-compose-buildx.yml up --build -d
        ;;
    
    clean-cache)
        print_status "Cleaning buildx cache..."
        docker buildx prune -f
        rm -rf /tmp/.buildx-cache-*
        print_status "Cache cleaned!"
        ;;
    
    *)
        show_usage
        ;;
esac
