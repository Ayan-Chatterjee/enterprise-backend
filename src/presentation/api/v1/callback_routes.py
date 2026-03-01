"""Callback API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.callback_repo_impl import CallbackRepositoryImpl
from src.application.use_cases.callback.create_callback import CreateCallbackUseCase
from src.application.dtos.callback_dto import CallbackCreateDTO, CallbackResponseDTO
from src.core.exceptions import NotFoundException

router = APIRouter(prefix="/callbacks", tags=["callbacks"])


@router.post("", response_model=CallbackResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_callback(
    dto: CallbackCreateDTO,
    session: AsyncSession = Depends(get_session)
) -> CallbackResponseDTO:
    """Create a new callback"""
    try:
        repository = CallbackRepositoryImpl(session)
        use_case = CreateCallbackUseCase(repository)
        result = await use_case.execute(dto)
        await session.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("", response_model=list[CallbackResponseDTO])
async def get_callbacks(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
) -> list[CallbackResponseDTO]:
    """Get all callbacks with pagination"""
    try:
        repository = CallbackRepositoryImpl(session)
        callbacks = await repository.get_all(skip=skip, limit=limit)
        return [
            CallbackResponseDTO(
                id=cb.id,
                contact_id=cb.contact_id,
                scheduled_at=cb.scheduled_at,
                status=cb.status,
                notes=cb.notes,
                assigned_to=cb.assigned_to,
                created_at=cb.created_at,
                updated_at=cb.updated_at,
            )
            for cb in callbacks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{callback_id}", response_model=CallbackResponseDTO)
async def get_callback(
    callback_id: int,
    session: AsyncSession = Depends(get_session)
) -> CallbackResponseDTO:
    """Get a specific callback by ID"""
    try:
        repository = CallbackRepositoryImpl(session)
        callback = await repository.get_by_id(callback_id)
        if not callback:
            raise NotFoundException(f"Callback with ID {callback_id} not found")
        return CallbackResponseDTO(
            id=callback.id,
            contact_id=callback.contact_id,
            scheduled_at=callback.scheduled_at,
            status=callback.status,
            notes=callback.notes,
            assigned_to=callback.assigned_to,
            created_at=callback.created_at,
            updated_at=callback.updated_at,
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
