class DocumentValidationError(Exception):
    """Raised when an uploaded document fails validation."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DocumentNotFoundError(Exception):
    """Raised when a requested document does not exist."""

    def __init__(self, message: str = "Document not found.") -> None:
        self.message = message
        self.status_code = 404
        super().__init__(message)


class PdfExtractionError(Exception):
    """Raised when PDF text extraction fails."""

    def __init__(self, message: str, status_code: int = 422) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)
