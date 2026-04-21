class ClawShireError(Exception):
    """Base exception for SDK and CLI errors."""


class ClawShireConfigError(ClawShireError):
    """Missing or invalid local configuration."""


class ClawShireAuthError(ClawShireError):
    """Authentication or authorization failed."""


class ClawShireApiError(ClawShireError):
    """The upstream API returned an error response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ClawShireNetworkError(ClawShireError):
    """Network failure while calling the upstream API."""
