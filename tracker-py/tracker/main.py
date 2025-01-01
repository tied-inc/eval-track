from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from tracker.logging_config import get_logger, setup_logging
from tracker.middleware import api_access_log_middleware, error_handling_middleware, secret_key_middleware
from tracker.integrations.fastapi import router
from tracker.settings import settings

# Set up centralized logging configuration
setup_logging()

# Get logger for this module
logger = get_logger(__name__)

app = FastAPI()
app.include_router(router)

# Register error handling middleware first
app.middleware("http")(error_handling_middleware)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions."""
    logger.error(f"Unhandled exception occurred: {exc}", extra={"error_type": type(exc).__name__})
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.warning(f"Validation error occurred: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP exception occurred: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.middleware("http")(secret_key_middleware)
app.middleware("http")(api_access_log_middleware)
if settings.eval_tracker_trusted_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.eval_tracker_trusted_hosts)
