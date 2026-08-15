"""CloudSentinel AI application entry point."""

from fastapi import FastAPI, Request
from app.core.logging import setup_logging
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.api.routes.kubernetes import router as kubernetes_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.incidents import router as incidents_router

setup_logging()

app = FastAPI(
    title="CloudSentinel AI",
    version="1.0.0",
    description=(
        "AI-powered cloud incident detection, "
        "root-cause analysis, and controlled response platform."
    ),
)


# ---------------------------------------------------------
# CORS
# Allow only the local React frontend
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Register application routes
# ---------------------------------------------------------

app.include_router(analyze_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(kubernetes_router)
app.include_router(incidents_router)


# ---------------------------------------------------------
# Validation error handler
# ---------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return a consistent validation error response."""

    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid request data",
            "status_code": 422,
            "details": exc.errors(),
        },
    )


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
async def root() -> dict[str, str]:
    """Return basic application information."""

    return {
        "service": "CloudSentinel AI",
        "version": "1.0.0",
        "status": "running",
    }