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
    try:
        repository = ContactRepositoryImpl(session)
        use_case = CreateContactUseCase(repository)
        result = await use_case.execute(dto)
        await session.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("", response_model=list[ContactResponseDTO])
async def get_contacts(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[ContactResponseDTO]:
    """Get all contacts with pagination"""
    try:
        repository = ContactRepositoryImpl(session)
        use_case = GetContactsUseCase(repository)
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{contact_id}", response_model=ContactResponseDTO)
async def get_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_session)
) -> ContactResponseDTO:
    """Get a specific contact by ID"""
    try:
        repository = ContactRepositoryImpl(session)
        contact = await repository.get_by_id(contact_id)
        if not contact:
            raise NotFoundException(f"Contact with ID {contact_id} not found")
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
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
