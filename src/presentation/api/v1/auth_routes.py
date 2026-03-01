"""Authentication API routes"""
from fastapi import APIRouter, HTTPException, status
from src.application.use_cases.auth.login_user import LoginDTO, LoginResponseDTO, LoginUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponseDTO)
async def login(dto: LoginDTO) -> LoginResponseDTO:
    """User login endpoint"""
    try:
        # Note: This is a placeholder. In a real implementation,
        # you would use dependency injection to get the user repository
        # use_case = LoginUserUseCase(user_repository)
        # return await use_case.execute(dto)
        raise NotImplementedError("Login endpoint requires proper integration")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
