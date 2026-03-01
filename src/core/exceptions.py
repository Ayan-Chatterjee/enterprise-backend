"""Global custom exceptions"""


class ApplicationException(Exception):
    """Base exception for the application"""
    
    def __init__(self, message: str, code: str = "APPLICATION_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Raised when validation fails"""
    
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message, code, 400)


class NotFoundException(ApplicationException):
    """Raised when a resource is not found"""
    
    def __init__(self, message: str, code: str = "NOT_FOUND"):
        super().__init__(message, code, 404)


class UnauthorizedException(ApplicationException):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Unauthorized", code: str = "UNAUTHORIZED"):
        super().__init__(message, code, 401)


class ForbiddenException(ApplicationException):
    """Raised when authorization fails"""
    
    def __init__(self, message: str = "Forbidden", code: str = "FORBIDDEN"):
        super().__init__(message, code, 403)


class ConflictException(ApplicationException):
    """Raised when there's a conflict (e.g., duplicate resource)"""
    
    def __init__(self, message: str, code: str = "CONFLICT"):
        super().__init__(message, code, 409)


class RepositoryException(ApplicationException):
    """Raised when repository operations fail"""
    
    def __init__(self, message: str, code: str = "REPOSITORY_ERROR"):
        super().__init__(message, code, 500)
