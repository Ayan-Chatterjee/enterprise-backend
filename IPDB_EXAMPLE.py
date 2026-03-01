"""
Example: How to Use iPDB for Debugging

This shows a working example of interactive debugging with iPDB.
To run this example:

1. Make sure ipdb is installed:
   pip install ipdb

2. Add 'import ipdb; ipdb.set_trace()' to any route in contact_routes.py

3. Start the server WITHOUT --reload:
   uvicorn src.main:app --host 127.0.0.1 --port 8000

4. Make a request in another terminal:
   curl http://localhost:8000/api/v1/contacts

5. The server terminal becomes an interactive debugger where you can:
   - Type variable names to inspect them
   - Use iPDB commands like 'n', 's', 'c', etc.
   - Call Python functions to test code
"""

# ============================================================================
# EXAMPLE 1: Adding iPDB to get_contacts endpoint
# ============================================================================

# In src/presentation/api/v1/contact_routes.py, modify get_contacts like this:

"""
@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    '''Get all contacts with pagination'''
    
    # 👇 ADD THIS LINE 👇
    import ipdb; ipdb.set_trace()  # Execution will pause here!
    
    print(f"Debug: skip={skip}, limit={limit}")
    repository = ContactRepositoryImpl(session)
    use_case = GetContactsUseCase(repository)
    return await use_case.execute(skip=skip, limit=limit)
"""

# ============================================================================
# EXAMPLE 2: Running the Debugger
# ============================================================================

"""
Terminal 1 - Start the server (WITHOUT --reload):
$ cd /Users/ayanchatterjee/Desktop/My\ Drive/Development/enterprise-application/backend
$ source venv/bin/activate
$ uvicorn src.main:app --host 127.0.0.1 --port 8000

Terminal 2 - Make a request:
$ curl http://localhost:8000/api/v1/contacts

Terminal 1 - Now shows the debugger:
> /path/to/contact_routes.py(45)get_contacts()
    -> repository = ContactRepositoryImpl(session)

ipdb> 
"""

# ============================================================================
# EXAMPLE 3: Common iPDB Commands
# ============================================================================

"""
When you're in the iPDB debugger, you can use these commands:

NAVIGATION:
  c          Continue execution
  n          Next line (step over)
  s          Step into function
  u          Go up one level in the call stack
  d          Go down one level in the call stack

INSPECTION:
  p skip                Print the value of 'skip'
  pp skip               Pretty print 'skip' (formatted)
  l                     List the code around current line
  w                     Where (show current position in call stack)

BREAKPOINTS:
  b <line>              Set breakpoint at line
  cl <num>              Clear breakpoint number
  disabled <num>        Disable breakpoint
  enabled <num>         Enable breakpoint

EXECUTING CODE:
  !<python code>        Execute Python code
  ? <object>            Get help on object

QUITTING:
  q                     Quit/exit the debugger
  h                     Help (list all commands)
"""

# ============================================================================
# EXAMPLE 4: Real Debugging Session
# ============================================================================

"""
Server Terminal Output:

> /Users/ayanchatterjee/Desktop/My Drive/Development/enterprise-application/backend/src/presentation/api/v1/contact_routes.py(45)get_contacts()
    -> repository = ContactRepositoryImpl(session)

ipdb> skip
0
ipdb> limit
20
ipdb> print(session)
<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x7f9c5e8b5a30>
ipdb> print(type(session).__name__)
AsyncSession
ipdb> print(session.info)
{}
ipdb> n
> /Users/ayanchatterjee/Desktop/My Drive/Development/enterprise-application/backend/src/presentation/api/v1/contact_routes.py(46)get_contacts()
    -> use_case = GetContactsUseCase(repository)
ipdb> n
> /Users/ayanchatterjee/Desktop/My Drive/Development/enterprise-application/backend/src/presentation/api/v1/contact_routes.py(47)get_contacts()
    -> return await use_case.execute(skip=skip, limit=limit)
ipdb> c
✅ SUCCESS: Found 4 contacts
127.0.0.1:51994 - "GET /api/v1/contacts HTTP/1.1" 200 OK
"""

# ============================================================================
# EXAMPLE 5: Conditional Debugging
# ============================================================================

"""
Sometimes you only want to debug when a specific condition is true:

@router.get("/{contact_id}", response_model=ContactResponseDTO)
async def get_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    '''Get a specific contact by ID'''
    
    # Only debug if contact_id is 1
    if contact_id == 1:
        import ipdb; ipdb.set_trace()
    
    repository = ContactRepositoryImpl(session)
    contact = await repository.get_by_id(contact_id)
    return ContactResponseDTO.from_orm(contact)
"""

# ============================================================================
# EXAMPLE 6: Debugging Exception Handling
# ============================================================================

"""
If you want to debug when an exception occurs:

@router.post("", response_model=ContactResponseDTO)
async def create_contact(
    dto: ContactCreateDTO,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    '''Create a new contact'''
    
    try:
        repository = ContactRepositoryImpl(session)
        use_case = CreateContactUseCase(repository)
        result = await use_case.execute(dto)
        await session.commit()
        return result
    except Exception as e:
        import ipdb; ipdb.set_trace()  # Debug the exception
        # Now you can inspect:
        # ipdb> print(e)
        # ipdb> print(type(e).__name__)
        # ipdb> print(str(e))
        raise
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Q: The debugger doesn't stop - I just see the response
A: Make sure you're NOT using --reload flag!
   Use: uvicorn src.main:app --host 127.0.0.1 --port 8000
   Not: uvicorn src.main:app --reload

Q: The debugger opens but I can't type
A: Make sure the server is running in the foreground
   Don't use: nohup, &, or background processes
   
Q: I pressed 'c' but nothing happens
A: The debugger might be waiting for more input
   Try pressing Enter a few times

Q: How do I know when I've hit the breakpoint?
A: The curl request will hang/pause
   The server terminal will show the ipdb prompt
   Type commands and press Enter

Q: Can I use Swagger UI with iPDB?
A: No - Swagger makes async requests the browser can't see terminal output
   Use curl or httpie instead
"""

# ============================================================================
# QUICK START: Copy-Paste Template
# ============================================================================

"""
Want to debug a specific endpoint? Use this template:

1. Open src/presentation/api/v1/contact_routes.py

2. Find the endpoint you want to debug (e.g., get_contacts)

3. Add this line at the start of the function:
   import ipdb; ipdb.set_trace()

4. Save the file

5. Start server WITHOUT --reload:
   uvicorn src.main:app --host 127.0.0.1 --port 8000

6. Make request in another terminal:
   curl http://localhost:8000/api/v1/contacts

7. Type in the server terminal:
   ipdb> variable_name       # View a variable
   ipdb> n                   # Next line
   ipdb> s                   # Step into
   ipdb> c                   # Continue
   ipdb> h                   # Help
   ipdb> q                   # Quit

That's it! You're now debugging!
"""
