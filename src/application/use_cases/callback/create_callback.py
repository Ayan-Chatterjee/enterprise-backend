"""Use cases for callback operations"""
from src.domain.entities.callback import Callback
from src.domain.repositories.callback_repo import CallbackRepository
from src.application.dtos.callback_dto import CallbackCreateDTO, CallbackResponseDTO


class CreateCallbackUseCase:
    """Use case for creating a new callback"""
    
    def __init__(self, repository: CallbackRepository):
        self.repository = repository
    
    async def execute(self, dto: CallbackCreateDTO) -> CallbackResponseDTO:
        """Execute the use case"""
        callback = Callback(
            contact_id=dto.contact_id,
            scheduled_at=dto.scheduled_at,
            notes=dto.notes,
            assigned_to=dto.assigned_to,
            status="pending"
        )
        
        created_callback = await self.repository.create(callback)
        return self._to_response(created_callback)
    
    @staticmethod
    def _to_response(callback: Callback) -> CallbackResponseDTO:
        """Convert entity to DTO"""
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
