#!/bin/bash

# Docker Build and Test Script for Team Task Manager

set -e

echo "=================================="
echo "Team Task Manager - Docker Build"
echo "=================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Generate secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(openssl rand -hex 32)
    echo -e "${YELLOW}Generated SECRET_KEY: ${SECRET_KEY}${NC}"
fi

# Function to build backend
build_backend() {
    echo -e "${GREEN}Building backend...${NC}"
    docker build -f Dockerfile.backend -t taskmanager-backend .
    echo -e "${GREEN}Backend built successfully!${NC}"
}

# Function to build frontend
build_frontend() {
    echo -e "${GREEN}Building frontend...${NC}"
    docker build -f Dockerfile.frontend -t taskmanager-frontend .
    echo -e "${GREEN}Frontend built successfully!${NC}"
}

# Function to run with docker-compose
run_compose() {
    echo -e "${GREEN}Starting services with docker-compose...${NC}"
    docker-compose up -d
    echo ""
    echo -e "${GREEN}Services started!${NC}"
    echo "Frontend: http://localhost"
    echo "Backend: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
}

# Function to stop services
stop_compose() {
    echo -e "${YELLOW}Stopping services...${NC}"
    docker-compose down
    echo -e "${GREEN}Services stopped!${NC}"
}

# Function to view logs
logs() {
    docker-compose logs -f
}

# Function to clean up
cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    docker-compose down -v
    docker system prune -f
    echo -e "${GREEN}Cleanup complete!${NC}"
}

# Main menu
case "$1" in
    backend)
        build_backend
        ;;
    frontend)
        build_frontend
        ;;
    build)
        build_backend
        build_frontend
        ;;
    up)
        run_compose
        ;;
    down)
        stop_compose
        ;;
    logs)
        logs
        ;;
    clean)
        cleanup
        ;;
    *)
        echo "Usage: $0 {backend|frontend|build|up|down|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  backend   - Build backend Docker image"
        echo "  frontend  - Build frontend Docker image"
        echo "  build     - Build both images"
        echo "  up        - Start services with docker-compose"
        echo "  down      - Stop services"
        echo "  logs      - View service logs"
        echo "  clean     - Clean up containers and volumes"
        exit 1
        ;;
esac
