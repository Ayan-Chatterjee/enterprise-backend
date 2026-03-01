"""Contact API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
from src.application.use_cases.contact.create_contact import CreateContactUseCase, GetContactsUseCase
from src.application.dtos.contact_dto import ContactCreateDTO, ContactResponseDTO
from src.core.exceptions import NotFoundException

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_contact(
    dto: ContactCreateDTO,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    """Create a new contact"""
    print(f"\n{'='*60}")
    print(f"🔍 DEBUG: create_contact() endpoint called")
    print(f"   - dto: {dto}")
    print(f"{'='*60}\n")
    
    try:
        repository = ContactRepositoryImpl(session)
        use_case = CreateContactUseCase(repository)
        result = await use_case.execute(dto)
        await session.commit()
        print(f"✅ SUCCESS: Contact created with ID {result.id}")
        return result
    except ValueError as e:
        print(f"❌ VALIDATION ERROR: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    print(f"\n{'='*60}")
    print(f"🔍 DEBUG: get_contacts() endpoint called")
    print(f"   - skip: {skip}")
    print(f"   - limit: {limit}")
    print(f"   - session type: {type(session)}")
    print(f"{'='*60}\n")
    
    try:
        repository = ContactRepositoryImpl(session)
        use_case = GetContactsUseCase(repository)
        result = await use_case.execute(skip=skip, limit=limit)
        print(f"✅ SUCCESS: Found {len(result)} contacts")
        return result
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{contact_id}", response_model=ContactResponseDTO)
async def get_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    """Get a specific contact by ID"""
    print(f"\n{'='*60}")
    print(f"🔍 DEBUG: get_contact() endpoint called")
    print(f"   - contact_id: {contact_id}")
    print(f"{'='*60}\n")
    
    try:
        repository = ContactRepositoryImpl(session)
        contact = await repository.get_by_id(contact_id)
        if not contact:
            print(f"❌ NOT FOUND: Contact with ID {contact_id} not found")
            raise NotFoundException(f"Contact with ID {contact_id} not found")
        print(f"✅ SUCCESS: Found contact {contact.first_name} {contact.last_name}")
        return ContactResponseDTO(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            message=contact.message,
            status=contact.status,
            source=contact.source,
            created_at=contact.created_at,
            updated_at=contact.updated_at,
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message) from e
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
