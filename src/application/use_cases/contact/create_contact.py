"""Use cases for contact operations"""
from src.domain.entities.contact import Contact
from src.domain.repositories.contact_repo import ContactRepository
from src.application.dtos.contact_dto import ContactCreateDTO, ContactResponseDTO
from typing import List


class CreateContactUseCase:
    """Use case for creating a new contact"""
    
    def __init__(self, repository: ContactRepository):
        self.repository = repository
    
    async def execute(self, dto: ContactCreateDTO) -> ContactResponseDTO:
        """Execute the use case"""
        contact = Contact(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email or "",
            phone=dto.phone or "",
            message=dto.message,
            source=dto.source,
            status="new"
        )
        
        created_contact = await self.repository.create(contact)
        return self._to_response(created_contact)
    
    @staticmethod
    def _to_response(contact: Contact) -> ContactResponseDTO:
        """Convert entity to DTO"""
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


class GetContactsUseCase:
    """Use case for fetching contacts"""
    
    def __init__(self, repository: ContactRepository):
        self.repository = repository
    
    async def execute(self, skip: int = 0, limit: int = 20) -> List[ContactResponseDTO]:
        """Execute the use case"""
        contacts = await self.repository.get_all(skip=skip, limit=limit)
        return [self._to_response(contact) for contact in contacts]
    
    @staticmethod
    def _to_response(contact: Contact) -> ContactResponseDTO:
        """Convert entity to DTO"""
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
