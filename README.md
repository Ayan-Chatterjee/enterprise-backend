# Real Estate Backend

A modern, scalable FastAPI backend application following Clean Architecture principles.

## Architecture Overview

```
real-estate-backend/
├── src/
│   ├── core/                 # Application-wide core logic
│   ├── domain/              # Pure business logic (entities, value objects, interfaces)
│   ├── application/         # Use cases and application logic
│   ├── infrastructure/      # External implementations (DB, cache, messaging)
│   ├── presentation/        # API endpoints and dependency injection
│   └── main.py             # FastAPI application entry point
├── tests/                   # Test suite
├── alembic/                # Database migrations
└── docker/                 # Docker configuration
```

## Features

- **FastAPI**: Modern async Python web framework
- **SQLAlchemy**: Async ORM with PostgreSQL support
- **Clean Architecture**: Separation of concerns with domain-driven design
- **Dependency Injection**: Loose coupling and testability
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic organization
- **Event-driven Ready**: Infrastructure for async messaging
- **Async-first Design**: Full async/await support
- **PostgreSQL**: Robust relational database
- **Redis**: Caching infrastructure (optional)
- **Pydantic**: Data validation and serialization
- **JWT Authentication**: Secure user authentication
- **Docker**: Containerization with Docker Compose
- **Structured Logging**: JSON-formatted logs
- **Error Handling**: Global exception handling
- **CORS Support**: Cross-origin resource sharing

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis (optional)
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository
```bash
cd backend
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### Using Docker Compose

```bash
cd docker
docker-compose up --build
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## Project Structure

### Core (`src/core/`)
- `config.py`: Environment configuration
- `exceptions.py`: Global custom exceptions
- `logging.py`: Structured logging setup
- `security.py`: JWT and password hashing utilities
- `middleware.py`: Global middleware configuration
- `constants.py`: Application constants

### Domain (`src/domain/`)
- `entities/`: Business entities (Contact, User, Callback)
- `value_objects/`: Immutable value objects (Email, Phone)
- `repositories/`: Abstract repository interfaces
- `services/`: Domain services (optional)

### Application (`src/application/`)
- `use_cases/`: Application use cases organized by domain
- `dtos/`: Data Transfer Objects for API requests/responses
- `interfaces/`: Application interfaces (Unit of Work pattern)

### Infrastructure (`src/infrastructure/`)
- `database/`: Database configuration, models, and session management
- `repositories/`: Concrete repository implementations
- `cache/`: Redis caching infrastructure
- `messaging/`: Message queue infrastructure (Kafka/RabbitMQ ready)

### Presentation (`src/presentation/`)
- `api/v1/`: API route handlers
- `dependencies.py`: Dependency injection setup

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "Add new table"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=src
```

### Run specific test file
```bash
pytest tests/unit/test_contact_entity.py
```

## Development

### Code Style
The project follows PEP 8 and uses modern Python practices.

### Adding a New Feature

1. **Create Entity** in `src/domain/entities/`
2. **Create Repository Interface** in `src/domain/repositories/`
3. **Create DTOs** in `src/application/dtos/`
4. **Create Use Cases** in `src/application/use_cases/`
5. **Implement Repository** in `src/infrastructure/repositories/`
6. **Create Database Model** in `src/infrastructure/database/models/`
7. **Create API Routes** in `src/presentation/api/v1/`
8. **Write Tests** in `tests/`

## Configuration

All configuration is managed through environment variables. See `.env` for available options.

### Key Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Security Considerations

1. Change `SECRET_KEY` in production
2. Use strong database passwords
3. Enable HTTPS in production
4. Implement rate limiting
5. Use environment variables for sensitive data
6. Enable CORS only for trusted origins

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

MIT License

## Support

For issues, questions, or suggestions, please open an issue on the repository.
