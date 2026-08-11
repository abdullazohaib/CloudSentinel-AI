"""CloudSentinel AI application entry point."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.api.routes.kubernetes import router as kubernetes_router
from app.api.routes.metrics import router as metrics_router


app = FastAPI(
    title="CloudSentinel AI",
    version="1.0.0",
    description=(
        "AI-powered cloud incident detection, "
        "root-cause analysis, and controlled response platform."
    ),
)


# Register application routes
app.include_router(analyze_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(kubernetes_router)


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


@app.get("/")
async def root() -> dict[str, str]:
    """Return basic application information."""

    return {
        "service": "CloudSentinel AI",
        "version": "1.0.0",
        "status": "running",
    }