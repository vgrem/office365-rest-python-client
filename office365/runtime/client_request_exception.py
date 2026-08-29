from __future__ import annotations

from typing import Optional

from requests import RequestException, Response

_HEADER_REQUEST_IDS = ("request-id", "client-request-id", "SPRequestGuid")


class ClientRequestException(RequestException):
    """Custom exception for client requests with enhanced error handling.

    In addition to ``code`` / ``message`` it surfaces correlation and server
    diagnostics when the error response provides them (Graph ``innerError``,
    ``request-id``; SharePoint ``SPRequestGuid`` / ``SPRequestDuration`` /
    ``X-SharePointHealthScore``).
    """

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

        if not isinstance(error, dict):
            error = {}

        details = error.get("details", [])
        code = error.get("code") or ""
        msg = error.get("message")
        msg_text = str(msg.get("value", "")) if isinstance(msg, dict) else str(msg or "")
        if (
            code in {"nameAlreadyExists", "ErrorFolderExists"}
            or any(d.get("code") == "ConflictingObjects" for d in details)
            or "183" in code
            or "-2130575342" in code  # SharePoint: list/survey/document library already exists
            or "already exists" in msg_text.lower()
        ):
            exc: ClientRequestException = DuplicatedObjectException(response=response)
        elif "-2147024809" in code:
            exc: ClientRequestException = ObjectNotFoundException(response=response)
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

    @property
    def inner_error(self) -> Optional[dict]:
        """The Graph ``innerError`` payload (``request-id``, ``date``, ...), if any."""
        inner = self._error.get("innerError")
        return inner if isinstance(inner, dict) else None

    @property
    def request_id(self) -> Optional[str]:
        """Correlation ID for the failed request, if reported.

        Prefers Graph/SharePoint response headers (``request-id``,
        ``client-request-id``, ``SPRequestGuid``), then the Graph
        ``innerError.request-id``.
        """
        headers = getattr(self.response, "headers", None) or {}
        for name in _HEADER_REQUEST_IDS:
            value = headers.get(name)
            if value:
                return value
        inner = self.inner_error or {}
        return inner.get("request-id")

    @property
    def server_guid(self) -> Optional[str]:
        """SharePoint server request GUID (``SPRequestGuid`` header)."""
        return (getattr(self.response, "headers", None) or {}).get("SPRequestGuid")

    @property
    def duration_ms(self) -> Optional[int]:
        """SharePoint server-side processing time (``SPRequestDuration``), ms."""
        return _to_int((getattr(self.response, "headers", None) or {}).get("SPRequestDuration"))

    @property
    def health_score(self) -> Optional[int]:
        """SharePoint server health score (``X-SharePointHealthScore``)."""
        return _to_int((getattr(self.response, "headers", None) or {}).get("X-SharePointHealthScore"))


def _to_int(value: object) -> Optional[int]:
    """Parse a header value into an int, returning None when absent/invalid."""
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


class DuplicatedObjectException(ClientRequestException):
    """Raised when creating an object that already exists (HTTP 400 + ConflictingObjects)."""


class ObjectNotFoundException(ClientRequestException):
    """Raised when a requested object is not found (HTTP 404 or ResourceNotFound code)."""
