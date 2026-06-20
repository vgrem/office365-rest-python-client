from __future__ import annotations

from typing import Optional

from requests import RequestException, Response


class ClientRequestException(RequestException):
    """Custom exception for client requests with enhanced error handling."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._error: dict = {}

    @classmethod
    def from_response(cls, response: Response) -> ClientRequestException:
        """Factory: parse error response, dispatch to the right exception type.

        Inspects the error payload once and returns a specific subclass
        (e.g. DuplicatedObjectException), so callers never deal with
        HTTP status codes or error JSON.
        """
        try:
            error = response.json().get("error", {})
        except Exception:
            error = {}

        details = error.get("details", [])
        if (
            error.get("code") == "nameAlreadyExists"
            or error.get("code") == "ErrorFolderExists"
            or any(d.get("code") == "ConflictingObjects" for d in details)
        ):
            exc: ClientRequestException = DuplicatedObjectException(response=response)
        else:
            exc = cls(response=response)

        exc._error = error
        if error:
            exc.args = (exc.code or "", exc.message or "")
        else:
            http_error_msg = f"{response.status_code} {response.reason} for url: {response.url}"
            exc.args = (str(response.status_code), http_error_msg)
        return exc

    @property
    def code(self) -> Optional[str]:
        return self._error.get("code")

    @property
    def message(self) -> str:
        msg = self._error.get("message")
        if isinstance(msg, dict):
            return str(msg.get("value", ""))
        return str(msg or "")

    @property
    def message_lang(self) -> Optional[str]:
        msg = self._error.get("message")
        return msg.get("lang") if isinstance(msg, dict) else None


class DuplicatedObjectException(ClientRequestException):
    """Raised when creating an object that already exists (HTTP 400 + ConflictingObjects)."""


class ObjectNotFoundException(ClientRequestException):
    """Raised when a requested object is not found (HTTP 404 or ResourceNotFound code)."""
