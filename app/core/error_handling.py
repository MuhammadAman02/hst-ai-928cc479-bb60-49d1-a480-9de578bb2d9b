"""
Error handling utilities for the application.
"""
from enum import Enum
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ErrorCode(str, Enum):
    """Application error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    PROCESSING_ERROR = "PROCESSING_ERROR"
    EXTERNAL_API_ERROR = "EXTERNAL_API_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ApplicationError(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, error_code: ErrorCode, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(ApplicationError):
    """Validation error."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, details)


class AuthenticationError(ApplicationError):
    """Authentication error."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, ErrorCode.AUTHENTICATION_ERROR, details)


class AuthorizationError(ApplicationError):
    """Authorization error."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, ErrorCode.AUTHORIZATION_ERROR, details)


class ResourceNotFoundError(ApplicationError):
    """Resource not found error."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, ErrorCode.RESOURCE_NOT_FOUND, details)


def register_exception_handlers(app: FastAPI):
    """Register exception handlers for the application."""
    
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError):
        """Handle application errors."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error_code=exc.error_code,
                message=exc.message,
                details=exc.details
            ).dict()
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error_code=ErrorCode.VALIDATION_ERROR,
                message="Validation error",
                details={"errors": exc.errors()}
            ).dict()
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="Internal server error",
                details={"error": str(exc)}
            ).dict()
        )