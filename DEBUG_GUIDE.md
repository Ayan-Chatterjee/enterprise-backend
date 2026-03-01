# API Request Debugging Guide

This guide explains how to debug API requests in the FastAPI backend, including tools, techniques, and common scenarios.

## Table of Contents
1. [Setup & Tools](#setup--tools)
2. [Logging Configuration](#logging-configuration)
3. [Interactive Debugging](#interactive-debugging)
4. [Common Debugging Techniques](#common-debugging-techniques)
5. [Endpoint-Specific Debugging](#endpoint-specific-debugging)
6. [Database Debugging](#database-debugging)
7. [Performance Debugging](#performance-debugging)
8. [Common Issues & Solutions](#common-issues--solutions)

---

## Setup & Tools

### Prerequisites
You should have:
- Virtual environment activated: `source venv/bin/activate`
- FastAPI server running or ability to start it: `uvicorn src.main:app --reload`
- Python debugger tools installed (already available: `pdb`, `ipdb` optional)

### Essential Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| `pdb` (Python Debugger) | Built-in, set breakpoints | Already available |
| `ipdb` | Enhanced pdb with autocomplete | `pip install ipdb` |
| `FastAPI Docs` | Interactive API docs | `http://localhost:8000/api/docs` |
| `curl` / `httpie` | Command-line HTTP testing | Built-in / `pip install httpie` |
| `Pydantic debugger` | Validate DTOs | Python REPL |
| `SQLAlchemy echo` | Log all SQL queries | Set `DATABASE_ECHO=true` in `.env` |

---

## Logging Configuration

### Enable SQL Query Logging

Edit `.env`:

```properties
DATABASE_ECHO=true
LOG_LEVEL=DEBUG
DEBUG=true
```

This will print all SQL queries to the console:

```
SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.email FROM contacts
```

### Check Current Logging Level

In `src/core/logging.py`, the logger is configured with `LOG_LEVEL` from env. Increase verbosity by setting:

```bash
export LOG_LEVEL=DEBUG  # or set in .env
```

Then restart the server:

```bash
uvicorn src.main:app --reload
```

### Log Output Locations

- **Console**: All logs print to stdout when running in development mode.
- **Production**: Logs go to stderr (configured in `src/core/logging.py`).

---

## Interactive Debugging

### 1. Using the FastAPI Swagger Docs

**Best for**: Quick testing without writing code.

1. Start the server: `uvicorn src.main:app --reload`
2. Visit: `http://localhost:8000/api/docs`
3. Click on an endpoint (e.g., `GET /api/v1/contacts`)
4. Click **Try it out**
5. Fill in parameters or request body
6. Click **Execute**
7. View the response, status code, and headers

**Advantages**:
- No need to write curl commands
- Auto-validates Pydantic models
- Shows response status and body clearly

### 2. Using curl for Low-Level Debugging

**Best for**: Testing headers, custom content types, and scripting.

#### List Contacts (GET)
```bash
curl -v http://localhost:8000/api/v1/contacts
```

The `-v` flag shows:
- Request headers
- Response headers
- Status code
- Response body

#### Create Contact (POST)
```bash
curl -X POST http://localhost:8000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "phone": "+1-555-0000",
    "message": "Debug test"
  }' \
  -v
```

#### With Authentication Header
```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
  http://localhost:8000/api/v1/contacts \
  -v
```

### 3. Using httpie (Pretty Alternative to curl)

**Installation**:
```bash
pip install httpie
```

**List Contacts**:
```bash
http GET localhost:8000/api/v1/contacts
```

**Create Contact**:
```bash
http POST localhost:8000/api/v1/contacts \
  first_name=Test \
  last_name=User \
  email=test@example.com
```

**With Headers**:
```bash
http --headers GET localhost:8000/api/v1/contacts
```

---

## Common Debugging Techniques

### 1. Add Print Statements in Route Handlers

Edit `src/presentation/api/v1/contact_routes.py`:

```python
@router.get("/contacts")
async def list_contacts(
    session: AsyncSession = Depends(get_db_session),
    skip: int = Query(0),
    limit: int = Query(10)
):
    print(f"🔍 DEBUG: Received request with skip={skip}, limit={limit}")
    
    try:
        contacts = await contact_repository.list(session, skip, limit)
        print(f"✅ DEBUG: Found {len(contacts)} contacts")
        return contacts
    except Exception as e:
        print(f"❌ DEBUG: Error occurred: {str(e)}")
        raise
```

Output in console:
```
🔍 DEBUG: Received request with skip=0, limit=10
✅ DEBUG: Found 3 contacts
```

### 2. Set a Breakpoint with pdb

Add `breakpoint()` in your code:

```python
@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: int, session: AsyncSession = Depends(get_db_session)):
    breakpoint()  # Execution pauses here
    contact = await contact_repository.get_by_id(session, contact_id)
    return contact
```

When you hit this endpoint, the terminal becomes an interactive debugger:

```
> /Users/.../src/presentation/api/v1/contact_routes.py(10)get_contact()
    -> contact = await contact_repository.get_by_id(session, contact_id)

(Pdb) contact_id
1
(Pdb) session
<AsyncSession object at 0x...>
(Pdb) continue
```

**Commands**:
- `p <var>` - Print variable
- `pp <var>` - Pretty print
- `continue` - Resume execution
- `step` - Step into next line
- `next` - Step over next line
- `list` - Show code
- `quit` - Exit debugger

### 3. Using ipdb for Better Debugging

Install ipdb:
```bash
pip install ipdb
```

Replace `breakpoint()` with:
```python
import ipdb; ipdb.set_trace()
```

Advantages: syntax highlighting, autocomplete, better experience.

### 4. Inspect Pydantic Models

In a Python REPL or script:

```python
from src.application.dtos.contact_dto import CreateContactDTO

# Valid data
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
contact = CreateContactDTO(**data)
print(contact)  # CreateContactDTO(first_name='John', ...)
print(contact.dict())  # {'first_name': 'John', ...}

# Invalid data
try:
    bad_data = {"first_name": "John"}  # Missing required field
    CreateContactDTO(**bad_data)
except Exception as e:
    print(f"Validation error: {e}")
```

---

## Endpoint-Specific Debugging

### Debug: GET /api/v1/contacts

**Scenario**: Not returning any contacts

**Steps**:

1. **Check if database is reachable**:
   ```bash
   python -c "
   import asyncio
   from src.infrastructure.database.session import engine
   
   async def test():
       async with engine.connect() as conn:
           result = await conn.execute('SELECT 1')
           print('✅ DB Connected')
   
   asyncio.run(test())
   "
   ```

2. **Check if table exists**:
   ```bash
   curl http://localhost:8000/api/v1/contacts -v
   # Look for HTTP status
   ```

3. **Enable SQL echo** in `.env`:
   ```
   DATABASE_ECHO=true
   ```
   Restart server and make the request. You'll see the SQL query:
   ```
   SELECT contacts.id, contacts.first_name, ... FROM contacts
   ```

4. **Check response status**:
   - `200` = Success, check response body
   - `404` = Route not found
   - `500` = Server error, check terminal logs
   - `422` = Invalid query parameters

### Debug: POST /api/v1/contacts

**Scenario**: Getting 422 Unprocessable Entity

**Steps**:

1. **Check the error message**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/contacts \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Test"}' \
     -v
   ```

   Response might be:
   ```json
   {
     "detail": [
       {
         "loc": ["body", "last_name"],
         "msg": "field required",
         "type": "value_error.missing"
       }
     ]
   }
   ```
   This tells you `last_name` is required.

2. **Validate payload manually**:
   ```python
   from src.application.dtos.contact_dto import CreateContactDTO
   
   payload = {"first_name": "Test"}
   try:
       dto = CreateContactDTO(**payload)
   except Exception as e:
       print(f"Validation error: {e}")
   ```

3. **Check database constraints**:
   If you get `409 Conflict`, it might be a unique constraint. Enable SQL echo to see the actual error.

---

## Database Debugging

### Enable SQLAlchemy Query Logging

Set `DATABASE_ECHO=true` in `.env` and restart the server.

Example output:
```
2026-03-01 14:00:00 INFO sqlalchemy.engine.Engine SELECT contacts.id, contacts.first_name, contacts.last_name FROM contacts
2026-03-01 14:00:00 INFO sqlalchemy.engine.Engine [cached statement]
```

### Check Database Connection Directly

```python
import asyncio
from src.infrastructure.database.session import AsyncSession, engine
from sqlalchemy import select, text

async def debug_db():
    async with AsyncSession(engine) as session:
        # Test connection
        result = await session.execute(text("SELECT 1"))
        print("✅ Connected")
        
        # Count contacts
        result = await session.execute(text("SELECT COUNT(*) FROM contacts"))
        count = result.scalar()
        print(f"Contacts in DB: {count}")

asyncio.run(debug_db())
```

Run from project root:
```bash
python << 'EOF'
import asyncio
from src.infrastructure.database.session import AsyncSession, engine
from sqlalchemy import text

async def debug_db():
    async with AsyncSession(engine) as session:
        result = await session.execute(text("SELECT COUNT(*) FROM contacts"))
        count = result.scalar()
        print(f"Contacts: {count}")

asyncio.run(debug_db())
EOF
```

### Inspect Raw Table Data

```bash
# Using psql directly (if installed)
psql -h db.qneuianspdpxfitqgbwc.supabase.co \
     -U postgres \
     -d postgres \
     -c "SELECT * FROM contacts;"
```

---

## Performance Debugging

### 1. Check Request Timing

```bash
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/api/v1/contacts
```

Shows total request time in seconds.

### 2. Add Timing to Routes

```python
import time
from src.core.logging import logger

@router.get("/contacts")
async def list_contacts(session: AsyncSession = Depends(get_db_session)):
    start = time.time()
    
    contacts = await contact_repository.list(session)
    
    elapsed = time.time() - start
    logger.info(f"list_contacts took {elapsed:.3f}s")
    
    return contacts
```

### 3. Use Python's `timeit` for Specific Operations

```python
import timeit
from src.application.use_cases.contact.create_contact import CreateContact

time_taken = timeit.timeit(
    lambda: CreateContact().execute(...),
    number=10
)
print(f"Average time: {time_taken / 10:.3f}s")
```

---

## Common Issues & Solutions

| Issue | Symptom | Debug Step | Solution |
|-------|---------|-----------|----------|
| DB not reachable | 500 error, connection timeout | Check `.env` `DATABASE_URL` | Verify Supabase credentials |
| Wrong endpoint | 404 Not Found | Check route path in `*_routes.py` | Verify endpoint matches request |
| Missing dependency | 500 error, dependency injection fails | Check `dependencies.py` | Ensure `Depends()` is used correctly |
| Validation error | 422 Unprocessable Entity | Check Pydantic DTO fields | Send all required fields |
| Unique constraint | 409 Conflict | Enable `DATABASE_ECHO=true` | Check if duplicate email/phone |
| Auth token invalid | 401 Unauthorized | Check `Authorization` header | Generate valid JWT or login first |
| CORS error | Browser shows CORS error | Check browser console and server logs | Verify `CORS_ORIGINS` in `.env` |
| Async issue | Runtime error or hang | Check for missing `await` | Use `await` on async functions |

---

## Step-by-Step Debugging Workflow

1. **Start with logging**
   - Set `LOG_LEVEL=DEBUG` and `DATABASE_ECHO=true` in `.env`
   - Restart server: `uvicorn src.main:app --reload`

2. **Make the request**
   - Use Swagger docs (`/api/docs`) or curl

3. **Read the response**
   - Note HTTP status code
   - Check response body for error details
   - Check server console for logs/queries

4. **Add breakpoint if needed**
   - Locate the route or use case
   - Add `breakpoint()` before the problematic line
   - Re-run the request and inspect variables in pdb

5. **Check the database**
   - Enable SQL echo to see queries
   - Count records manually
   - Look for unique constraint violations

6. **Isolate the problem**
   - Is it in validation (Pydantic)?
   - Is it in business logic (use case)?
   - Is it in the database (repository)?

7. **Fix and test**
   - Make the change
   - Re-run the request
   - Confirm the issue is resolved

---

## Quick Reference: Debug Commands

```bash
# Start server with debug logging
export LOG_LEVEL=DEBUG DATABASE_ECHO=true
uvicorn src.main:app --reload

# Test endpoint with verbose output
curl -v http://localhost:8000/api/v1/contacts

# Test with POST and body
curl -X POST http://localhost:8000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com"}'

# Check database connection
python -c "
import asyncio
from src.infrastructure.database.session import AsyncSession, engine
from sqlalchemy import text

async def test():
    async with AsyncSession(engine) as session:
        result = await session.execute(text('SELECT 1'))
        print('✅ DB OK')

asyncio.run(test())
"

# View API docs in browser
open http://localhost:8000/api/docs

# Check current environment variables
env | grep -E "DATABASE|LOG_LEVEL|DEBUG"
```

---

## Summary

- **For quick tests**: Use Swagger UI at `/api/docs`
- **For detailed info**: Enable `DATABASE_ECHO=true` and `LOG_LEVEL=DEBUG`
- **For step-through debugging**: Use `breakpoint()` or `ipdb`
- **For curl testing**: Use `-v` flag and inspect status + body
- **For database issues**: Check SQL echo output and connection string

Happy debugging! 🐛