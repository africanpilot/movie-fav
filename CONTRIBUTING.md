# Contributing to Movie-Fav

Thank you for your interest in contributing to Movie-Fav! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Please read and follow our Code of Conduct.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Docker & Docker Desktop
- Python 3.13+
- Node.js 20+
- Poetry (Python dependency management)
- Yarn (Node.js package manager)
- Git

### Setup Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/movie-fav.git
   cd movie-fav
   ```
3. **Set up environment:**
   ```bash
   cp sample-env .dev.env
   # Edit .dev.env with your settings
   ```
4. **Install dependencies:**
   ```bash
   cd microservices
   poetry install
   yarn install
   ```
5. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branching Strategy

- `master` - Production-ready code
- `develop` - Integration branch for features
- `feature/feature-name` - Feature development
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes

### Making Changes

1. **Create a feature branch:**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run tests and quality checks:**

   ```bash
   # Run pre-commit hooks
   pre-commit run --all-files

   # Run Python tests
   cd microservices
   poetry run pytest --benchmark-disable -v

   # Run Node.js tests
   yarn test
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(auth): add OAuth2 integration
fix(movie): resolve duplicate movie entries
docs: update API documentation
test(user): add unit tests for user service
```

## Coding Standards

### Python

- **Style**: Follow PEP 8 (enforced by Black with 120 char line length)
- **Type hints**: Use type hints for all function parameters and returns
- **Docstrings**: Use Google-style docstrings for functions and classes
- **Imports**: Use isort for import sorting
- **Security**: Follow secure coding practices (enforced by Bandit)

**Example:**

```python
from typing import List, Optional

def get_user_movies(user_id: int, limit: Optional[int] = None) -> List[Movie]:
    """Get movies for a specific user.

    Args:
        user_id: The ID of the user
        limit: Maximum number of movies to return

    Returns:
        List of Movie objects

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    # Implementation here
    pass
```

### TypeScript/JavaScript

- **Style**: Use Prettier for formatting
- **Linting**: Follow ESLint configuration
- **Types**: Use TypeScript for all new code
- **Components**: Use functional components with hooks

**Example:**

```typescript
interface UserMoviesProps {
  userId: number;
  limit?: number;
}

export const UserMovies: React.FC<UserMoviesProps> = ({ userId, limit }) => {
  // Implementation here
};
```

### GraphQL

- **Schema**: Use schema-first approach
- **Naming**: Use camelCase for fields, PascalCase for types
- **Documentation**: Add descriptions to all fields and types

## Testing

### Test Requirements

- **Coverage**: Maintain minimum 80% test coverage
- **Types**: Write unit, integration, and end-to-end tests
- **Naming**: Use descriptive test names

### Python Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run coverage run -m pytest
poetry run coverage report

# Run specific tests
poetry run pytest apps/movie/test/
```

### JavaScript Testing

```bash
# Run all tests
yarn test

# Run with coverage
yarn test --coverage

# Run specific tests
yarn test UserMovies.test.tsx
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Update CHANGELOG.md** if applicable
4. **Ensure all checks pass:**
   - Pre-commit hooks
   - Unit tests
   - Integration tests
   - Code coverage thresholds

### Pull Request Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** must pass
2. **At least one reviewer** approval required
3. **Address feedback** promptly
4. **Squash commits** before merging

## Issue Reporting

### Bug Reports

Include:

- **Environment details** (OS, Docker version, etc.)
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots/logs** if applicable

### Feature Requests

Include:

- **Use case description**
- **Proposed solution**
- **Alternative solutions considered**
- **Additional context**

### Security Issues

**Do not create public issues for security vulnerabilities.**
Email: security@movie-fav.com

## Development Tips

### Useful Commands

```bash
# Start development environment
./run.sh docker dev up

# View logs
docker-compose -f docker-compose-dev.yml logs -f

# Run database migrations
cd microservices/apps/movie
poetry run alembic upgrade head

# Generate GraphQL schema
cd microservices/apps/theater
yarn compile
```

### Debugging

- Use VS Code debugger with provided configurations
- Check Docker logs for service issues
- Use GraphQL playground for API testing

## Getting Help

- **Documentation**: Check DEVELOPMENT.md
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Search existing issues before creating new ones
- **Contact**: maintainers@movie-fav.com

## Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Special mentions in documentation

Thank you for contributing to Movie-Fav! 🎬
