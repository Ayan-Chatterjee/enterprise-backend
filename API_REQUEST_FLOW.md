# API Request Flow

This document describes the request/response flow for the FastAPI backend (Clean Architecture). It explains what happens from the moment a client calls an API endpoint through to the database and back, including middleware, dependency injection, validation, authentication, logging, and error handling.

## Purpose / Contract

- Inputs: HTTP requests to endpoints under `/api/v1/*` (JSON payloads, query params, path params, headers, cookies).
- Outputs: JSON responses with proper HTTP status codes and error structures; side effects such as DB writes, cache updates, or messages may occur.
- Success criteria: Endpoint responds with 2xx on valid input and performs expected side effects; errors are returned with 4xx/5xx codes and clear messages.

## High-level sequence (short)

1. Client sends HTTP request to the API (e.g., `GET /api/v1/contacts`).
2. Uvicorn receives request and passes to FastAPI application.
3. FastAPI routing selects the matching path operation function in `src/presentation/api/v1/*`.
4. Dependency injection resolves route dependencies defined in `dependencies.py` (e.g., DB session, current user).
5. Request body and query params are validated/parsed into Pydantic models (DTOs) defined in `src/application/dtos`.
6. Route handler calls an application-level use case in `src/application/use_cases/*` (business logic orchestrator).
7. Use case invokes domain logic and calls repository interfaces (defined in `src/domain/repositories/*`).
8. Infrastructure repository implementation (in `src/infrastructure/repositories/*`) performs DB operations via the async SQLAlchemy session from `src/infrastructure/database/session.py`.
9. Database (Supabase/Postgres) executes queries and returns results.
10. Repositories map DB rows to domain entities or DTOs and return them up the stack.
11. Use case returns domain result to the route handler.
12. Route handler returns a Pydantic response model (or FastAPI `JSONResponse`) to the client.
13. Middleware or exception handlers may log the request/response and handle errors uniformly.

## Detailed flow with components

### 1) Inbound HTTP handling
- Server: `uvicorn` runs the FastAPI app in `src/main.py`.
- FastAPI receives request and matches the route (e.g., route defined in `src/presentation/api/v1/contact_routes.py`).

### 2) Middleware
- Global middleware in `src/core/middleware.py` runs before and after the route handler.
- Typical responsibilities: request logging, correlation ids, timing, CORS handling, error translation.

### 3) Dependency Injection
- Route dependencies are defined using FastAPI `Depends()` in `src/presentation/dependencies.py`.
- Common dependencies: async DB session (from `session.py`), current authenticated user (via `security.py`), configuration (`config.py`).

### 4) Validation and Parsing
- FastAPI auto-validates request bodies and query params against Pydantic DTOs in `src/application/dtos`.
- Validation errors return HTTP 422 with error details.

### 5) Authentication & Authorization
- If the route requires authentication, a dependency verifies JWT tokens (using `SECRET_KEY` and `ALGORITHM` from env) and returns a `User` domain object or raises `HTTPException(401)`.
- Authorization checks (roles/permissions) occur in the use case or before invoking critical actions.

### 6) Route Handler (Presentation Layer)
- The handler adapts HTTP-level concerns into application-level calls.
- It constructs inputs for the use case (DTOs) and calls the use case function/class.
- Example: `create_contact` route will collect `CreateContactDTO` and call the `CreateContact` use case.

### 7) Use Case (Application Layer)
- Implements orchestration and application workflow.
- Validates any additional business rules and calls repository methods.
- Does not depend on infrastructure details; it depends on repository interfaces.

### 8) Repository (Domain Interfaces / Infrastructure Implementation)
- Interface defined in `src/domain/repositories/*` (contracts).
- Concrete implementation in `src/infrastructure/repositories/*` uses SQLAlchemy models in `src/infrastructure/database/models/*`.
- Repositories convert domain entities to/from DB models.

### 9) Database Interaction
- Async SQLAlchemy `async_sessionmaker` is used with `asyncpg` driver.
- Typical pattern: `async with session.begin(): await session.execute(...)` or using repository methods which open/close sessions.
- Transactions are used for multi-step operations to guarantee atomicity.

### 10) Response Construction
- Repositories return domain objects to the use case; use case returns DTOs or primitives.
- Route handler returns Pydantic response models which FastAPI serializes to JSON.

### 11) Error Handling
- Validation errors: 422 Unprocessable Entity (FastAPI/Pydantic).
- Authentication errors: 401 Unauthorized.
- Authorization errors: 403 Forbidden.
- Not found: 404 Not Found (raise HTTPException(404)).
- Unexpected: 500 Internal Server Error (handled by global exception handler and logged).

## Example Flows

### A) GET /api/v1/contacts (List contacts)
1. Client: `GET /api/v1/contacts`
2. FastAPI route in `contact_routes.py` triggers `list_contacts` handler.
3. Dependencies resolve DB session.
4. Handler calls `ContactRepository.list()` (via use case).
5. Repository runs `SELECT ... FROM contacts;` via SQLAlchemy async session.
6. DB returns rows; repository maps rows to DTOs.
7. Handler returns list of contact DTOs as JSON with 200 status.

Example response:

```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "status": "new",
    "created_at": "2026-03-01T14:40:35.853106Z"
  }
]
```

### B) POST /api/v1/contacts (Create contact)
1. Client: `POST /api/v1/contacts` with JSON body.
2. FastAPI validates body against `CreateContactDTO`.
3. Handler calls `CreateContact` use case with DTO and DB session dependency.
4. Use case may enforce business rules (e.g., deduplicate by email).
5. Repository inserts new `Contact` row and commits transaction.
6. DB returns created ID; repository returns created domain entity.
7. Handler returns 201 Created with the created resource (or location header + 204 depending on design).

Example request:

```json
{
  "first_name": "Alice",
  "last_name": "Lee",
  "email": "alice.lee@example.com",
  "phone": "+1-555-6789",
  "message": "Interested in property"
}
```

Example response (201):

```json
{
  "id": 4,
  "first_name": "Alice",
  "last_name": "Lee",
  "email": "alice.lee@example.com",
  "status": "new"
}
```

## Logging and Observability
- Structured logs are emitted by `src/core/logging.py`.
- Log request id, method, path, status code, and timing in middleware.
- Errors include stack traces in server logs; sanitized errors are returned to clients.

## Caching and Async Considerations
- For heavy read endpoints, a cache layer (`src/infrastructure/cache/redis_client.py`) can be added to improve performance.
- All DB calls are async to avoid blocking the event loop; ensure long-running tasks are delegated to background workers.

## Testing Tips
- Use `tests/` to write unit tests for domain entities and use cases.
- Use integration tests with a test database (or testcontainers) for repository behavior.
- Mock external services (Redis, external APIs) in unit tests.

## Edge Cases and Common Failures
- DB connection failures: App should return 500. Use startup checks to fail fast if DB unreachable.
- Unique constraint violations: Return 409 Conflict with message.
- Large payloads: Validate size limits and return 413 if too large (or handle gracefully).
- Partial failures in multi-step use cases: Use transactions so partial writes don't persist.

## Quick Sequence Diagram (ASCII)

Client -> Uvicorn -> FastAPI Router -> Middleware -> Route Handler -> Use Case -> Repository -> DB
DB --> Repository --> Use Case --> Route Handler --> Middleware --> Client

## Summary
This project follows Clean Architecture: presentation layer (FastAPI routes + dependencies) calls application use cases which depend on repository interfaces. Infrastructure implements repositories using async SQLAlchemy and talks to PostgreSQL. This keeps business logic decoupled from persistence and makes the codebase testable and maintainable.

If you want, I can:
- Add this file to the repo (committing & pushing),
- Add a short flow diagram in PlantUML or Mermaid and include it in the README,
- Or generate quick integration tests for the two example endpoints.

Which next step would you prefer?