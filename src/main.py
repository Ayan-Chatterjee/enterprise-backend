"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import get_settings
from src.core.logging import configure_logging, get_logger
from src.core.exceptions import ApplicationException
from src.core.middleware import add_middlewares, exception_handler
from src.presentation.api.v1 import contact_routes, callback_routes, auth_routes

# Initialize settings and logging
settings = get_settings()
configure_logging(level=settings.log_level)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Add middlewares
add_middlewares(app)

# Add exception handler
app.add_exception_handler(ApplicationException, exception_handler)


# Include routers
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    print("Health check endpoint called")
    return {"status": "ok", "message": "Server is running"}


app.include_router(contact_routes.router, prefix="/api/v1")
app.include_router(callback_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Application startup")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Application shutdown")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
