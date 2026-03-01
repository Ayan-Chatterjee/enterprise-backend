"""Use cases for authentication"""
from src.domain.entities.user import User
from src.domain.repositories.user_repo import UserRepository
from src.core.security import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    """DTO for login request"""
    email: EmailStr
    password: str


class LoginResponseDTO(BaseModel):
    """DTO for login response"""
    access_token: str
    token_type: str = "bearer"


class LoginUserUseCase:
    """Use case for user login"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def execute(self, dto: LoginDTO) -> LoginResponseDTO:
        """Execute the use case"""
        # Find user by email
        user = await self.repository.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        
        return LoginResponseDTO(access_token=access_token)
