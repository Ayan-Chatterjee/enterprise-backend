"""Global middleware configuration"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.core.exceptions import ApplicationException
from src.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


def add_middlewares(app: FastAPI) -> None:
    """Add global middlewares to the FastAPI application"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def exception_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    """Handle application exceptions"""
    logger.error(
        f"Application error: {exc.code}",
        extra={
            "status_code": exc.status_code,
            "message": exc.message,
            "path": request.url.path,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )
