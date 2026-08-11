"""Application-specific exceptions."""


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AnalysisException(AppException):
    """Raised when incident analysis cannot be completed."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)