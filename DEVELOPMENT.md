# Movie-Fav Development Guide

## Overview

Movie-Fav is a microservices-based application for managing movie favorites, built with Python (FastAPI, GraphQL) backend services and Next.js frontend.

## Quick Start

### Prerequisites

- Docker & Docker Desktop
- Python 3.13+
- Node.js 20+
- Poetry (Python dependency management)
- Yarn (Node.js package manager)

### Initial Setup

1. **Clone and setup environment:**

   ```bash
   git clone <repository-url>
   cd movie-fav
   cp sample-env .dev.env
   # Edit .dev.env with your configuration
   ```

2. **Start development environment:**

   ```bash
   ./run.sh docker dev up
   ```

3. **Install development dependencies:**

   ```bash
   # Python dependencies
   cd microservices && poetry install

   # Node.js dependencies
   yarn install
   ```

## Development Workflow

### Code Quality

This project uses several tools to maintain code quality:

- **Pre-commit hooks**: Automatically run on commit
- **Black**: Python code formatting (120 char line length)
- **Flake8**: Python linting
- **isort**: Import sorting
- **Prettier**: JavaScript/TypeScript formatting
- **ESLint**: JavaScript/TypeScript linting
- **Bandit**: Security scanning for Python

### Running Tests

```bash
# Python tests
cd microservices
poetry run pytest --benchmark-disable -v

# Run all quality checks
pre-commit run --all-files

# Run specific service tests
make test MICROSERVICE_PATH=apps/movie
```

### Development Commands

```bash
# Start specific service
./run.sh docker dev up movie

# View logs
docker-compose -f docker-compose-dev.yml logs -f

# Run database migrations
cd microservices/apps/<service>
poetry run alembic upgrade head

# Generate GraphQL schema
cd microservices/apps/theater
yarn compile
```

## Architecture

### Microservices Structure

```
microservices/
├── apps/
│   ├── account/          # User authentication
│   ├── movie/            # Movie data service
│   ├── person/           # Person/actor data
│   ├── shows/            # TV shows service
│   ├── theater/          # Frontend Next.js app
│   ├── notifications/    # Notification service
│   └── apollo/           # GraphQL gateway
├── links/                # Shared libraries
└── packages/             # Shared packages
```

### Key Technologies

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis, RabbitMQ
- **Frontend**: Next.js, React, Apollo Client, Tailwind CSS
- **GraphQL**: Ariadne (Python), Apollo Server
- **Authentication**: Auth0, JWT
- **Deployment**: Docker, Kubernetes, Helm

## Environment Configuration

### Environment Files

- `.dev.env` - Development environment
- `.test.env` - Testing environment
- `.prod.env` - Production environment

### Key Environment Variables

```bash
# Database
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Auth0
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret

# External APIs
IMDB_API_KEY=your_imdb_key
SENDGRID_API_KEY=your_sendgrid_key
```

## Deployment

### Local Development

```bash
./run.sh docker dev up
```

### Testing Environment

```bash
./run.sh docker test up
```

### Production Deployment

```bash
# Using Helm
./run.sh deploy prod up

# Direct Docker
./run.sh docker prod up
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Check if ports 5432, 6379, 8000 are available
2. **Permission issues**: Ensure Docker has proper permissions
3. **Module not found**: Run `poetry install` in microservices directory
4. **Database connection**: Verify PostgreSQL is running and accessible

### Debugging

- Use VS Code debugger with provided configurations
- Check Docker logs: `docker-compose logs -f <service>`
- Enable debug mode: Set `DEBUG=true` in environment

### Performance Monitoring

- Health checks available at `/health` endpoints
- Metrics exposed for Prometheus monitoring
- Logging configured with structured format

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** with tests
4. **Run quality checks**: `pre-commit run --all-files`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**

### Code Style

- Follow PEP 8 for Python (enforced by Black/Flake8)
- Use TypeScript for new frontend code
- Write tests for new features
- Update documentation as needed

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
