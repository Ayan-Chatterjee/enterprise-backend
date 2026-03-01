# Practical Debugging Guide for FastAPI

This guide provides **actual working solutions** for debugging your FastAPI application.

## The Real Problem

Native Python `breakpoint()` and VS Code debugger don't work well with:
- Uvicorn's async event loop
- FastAPI's dependency injection
- Swagger UI's async requests

But there are **several proven methods that DO work**.

---

## Method 1: iPDB Interactive Debugger (WORKS!) ✅ **RECOMMENDED**

### Install iPDB
```bash
pip install ipdb
```

### Add to Your Route
```python
@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    
    # Add this line where you want to debug
    import ipdb; ipdb.set_trace()
    
    print(f"Skip: {skip}, Limit: {limit}")
    repository = ContactRepositoryImpl(session)
    use_case = GetContactsUseCase(repository)
    return await use_case.execute(skip=skip, limit=limit)
```

### Run Server (IMPORTANT: NO `--reload`)
```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000
```

### Make Request and Debug
```bash
# In another terminal
curl http://localhost:8000/api/v1/contacts
```

### The Terminal Shows Interactive Debugger
```
> /path/to/contact_routes.py(45)get_contacts()
    -> repository = ContactRepositoryImpl(session)

ipdb> skip
0
ipdb> limit
20
ipdb> print(session)
<AsyncSession object at 0x...>
ipdb> continue
```

**Commands in ipdb:**
- `p <variable>` - Print variable
- `pp <variable>` - Pretty print
- `n` - Next line
- `s` - Step into function
- `c` or `continue` - Resume execution
- `l` - List code
- `h` - Help

---

## Method 2: VS Code Python Debugger (WORKS!) ✅ **BEST EXPERIENCE**

### Step 1: Install debugpy
```bash
pip install debugpy
```

### Step 2: Create `.vscode/launch.json`
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI Debug",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false,
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/Users/ayanchatterjee/Desktop/My Drive/Development/enterprise-application/backend"
    }
  ]
}
```

### Step 3: Add Breakpoint in Code
Click in the left margin next to a line number in `contact_routes.py`:

```python
@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    # 🔴 Click here (left margin) to set breakpoint
    repository = ContactRepositoryImpl(session)
    use_case = GetContactsUseCase(repository)
    return await use_case.execute(skip=skip, limit=limit)
```

### Step 4: Press F5 to Start Debugging
- Uvicorn starts in VS Code's integrated terminal
- Red dot appears at breakpoint
- Make a curl request: `curl http://localhost:8000/api/v1/contacts`
- Execution pauses at breakpoint

### Step 5: Debug Controls
- **F10** - Step over (next line)
- **F11** - Step into (enter function)
- **Shift+F11** - Step out (exit function)
- **F5** - Continue execution
- **Ctrl+Shift+D** - Open debug panel to inspect variables

**Variable Panel Shows:**
- All local variables
- Their types and values
- Watch expressions

---

## Method 3: Strategic Print Debugging (SIMPLE & FAST) ✅

For quick debugging without fancy tools:

```python
@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    
    # ===== DEBUG BLOCK START =====
    import json
    debug_info = {
        "skip": skip,
        "limit": limit,
        "session_type": str(type(session)),
        "session_id": id(session)
    }
    print("\n" + "="*70)
    print("🔍 DEBUG: get_contacts() called")
    print(json.dumps(debug_info, indent=2, default=str))
    print("="*70 + "\n")
    # ===== DEBUG BLOCK END =====
    
    repository = ContactRepositoryImpl(session)
    use_case = GetContactsUseCase(repository)
    result = await use_case.execute(skip=skip, limit=limit)
    
    print(f"✅ Result: {len(result)} contacts found\n")
    return result
```

**To disable debugging:** Comment out or wrap in `if os.getenv('DEBUG'):`

---

## Method 4: Logging with Introspection (PRODUCTION-READY) ✅

```python
import logging
import inspect

logger = logging.getLogger(__name__)

@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    
    # Get current function info
    frame = inspect.currentframe()
    func_name = frame.f_code.co_name
    line_number = frame.f_lineno
    
    logger.debug(f"Function {func_name}() called at line {line_number}")
    logger.debug(f"Arguments: skip={skip}, limit={limit}")
    logger.debug(f"Session type: {type(session).__name__}")
    
    try:
        repository = ContactRepositoryImpl(session)
        use_case = GetContactsUseCase(repository)
        result = await use_case.execute(skip=skip, limit=limit)
        logger.debug(f"Success: Found {len(result)} contacts")
        return result
    except Exception as e:
        logger.error(f"Error in {func_name}: {str(e)}", exc_info=True)
        raise
```

**Enable debugging:**
```bash
export LOG_LEVEL=DEBUG
uvicorn src.main:app
```

---

## Method 5: Python REPL Testing (TEST BEFORE DEPLOYING) ✅

Test your code interactively before deploying:

```bash
python
```

```python
>>> import asyncio
>>> from src.infrastructure.database.session import AsyncSession, engine
>>> from src.infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
>>> from src.application.use_cases.contact.create_contact import GetContactsUseCase
>>> 
>>> async def test():
...     async with AsyncSession(engine) as session:
...         repo = ContactRepositoryImpl(session)
...         use_case = GetContactsUseCase(repo)
...         result = await use_case.execute(skip=0, limit=20)
...         print(f"Found {len(result)} contacts")
...         for contact in result:
...             print(f"  - {contact.first_name} {contact.last_name}")
...
>>> asyncio.run(test())
Found 4 contacts
  - John Doe
  - Jane Smith
  - Michael Johnson
  - Ayan Chatt
>>>
```

---

## Quick Reference Table

| Method | Setup Time | Ease | Works w/ Swagger | Works w/ curl | Best For |
|--------|-----------|------|-----------------|-------------|----------|
| iPDB | 2 min | ⭐⭐⭐ | ❌ | ✅ | Quick debugging |
| VS Code | 5 min | ⭐⭐ | ✅ | ✅ | Complete IDE experience |
| Print | 1 min | ⭐⭐⭐⭐ | ✅ | ✅ | Fast iteration |
| Logging | 3 min | ⭐⭐⭐ | ✅ | ✅ | Production-ready |
| REPL | 2 min | ⭐⭐⭐ | N/A | N/A | Unit testing |

---

## My Recommendation: Start Here

### Step 1: Quick Debug (Right Now)
Use **Method 3 (Print Debugging)**:
- No setup needed
- Works immediately
- See output in terminal

### Step 2: Better Debugging (Next Hour)
Install **iPDB** and use **Method 1**:
- Interactive variable inspection
- Step through code
- Proper debugger experience

### Step 3: Best Practice (When You Have Time)
Set up **VS Code Debugger** using **Method 2**:
- Click to set breakpoints
- Hover variables to see values
- Professional debugging experience

---

## Troubleshooting

### "Debugger hangs when I hit breakpoint"
- Make sure you're **NOT using `--reload`**
- Restart the server: `uvicorn src.main:app` (no flags)

### "Can't see output in Swagger"
- Swagger makes async requests in browser
- Use **curl** or **ipdb** instead
- Or enable logging to see output in server terminal

### "iPDB not responding"
- Check that uvicorn is running in foreground (not background)
- Terminal must be attached to process
- Don't use `nohup` or `&` when debugging

### "VS Code breakpoint doesn't work"
- Make sure `.vscode/launch.json` has correct `cwd` path
- Check Python extension is installed
- Press F5 to start debugging (not just Run)

---

## Complete Example: Debugging a POST Request

### Code with Debug Points
```python
@router.post("", response_model=ContactResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_contact(
    dto: ContactCreateDTO,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    """Create a new contact"""
    
    # DEBUG 1: Check input
    import ipdb; ipdb.set_trace()  # Pauses here
    # Now in ipdb, you can:
    # ipdb> print(dto)
    # ipdb> print(dto.first_name)
    # ipdb> print(type(session))
    
    try:
        repository = ContactRepositoryImpl(session)
        use_case = CreateContactUseCase(repository)
        
        # DEBUG 2: Check before execution
        print(f"About to create contact: {dto.first_name} {dto.last_name}")
        
        result = await use_case.execute(dto)
        
        # DEBUG 3: Check result
        print(f"Created contact with ID: {result.id}")
        print(f"Result object: {result}")
        
        await session.commit()
        return result
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        await session.rollback()
        raise
```

### Test It
```bash
# Terminal 1: Start server
uvicorn src.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Make request
curl -X POST http://localhost:8000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com"
  }'

# Terminal 1: Shows interactive debugger
```

---

## Summary

**Don't use native `breakpoint()`** — it doesn't work well with async FastAPI.

**Use instead:**
1. **iPDB** for interactive debugging (Method 1)
2. **VS Code** for best IDE experience (Method 2)
3. **Print statements** for quick debugging (Method 3)

All three are proven to work. Pick one and start debugging! 🎯