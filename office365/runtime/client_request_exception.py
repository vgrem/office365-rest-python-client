from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from requests import RequestException, Response

_HEADER_REQUEST_IDS = ("request-id", "client-request-id", "SPRequestGuid")


@dataclass(frozen=True)
class ErrorPayload:
    """Normalized view of an OData error response, parsed once for classification."""

    code: str = ""
    message: str = ""
    details: tuple[dict, ...] = ()
    status: Optional[int] = None


def _parse_error(response: Response) -> dict:
    try:
        error = response.json().get("error", {})
    except Exception:
        return {}
    return error if isinstance(error, dict) else {}


def _to_payload(error: dict, response: Response) -> ErrorPayload:
    msg = error.get("message")
    message = str(msg.get("value", "")) if isinstance(msg, dict) else str(msg or "")
    details = error.get("details")
    return ErrorPayload(
        code=str(error.get("code") or ""),
        message=message,
        details=tuple(d for d in details if isinstance(d, dict)) if isinstance(details, list) else (),
        status=getattr(response, "status_code", None),
    )


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
    def matches(cls, payload: ErrorPayload) -> bool:
        """Whether this exception type describes the given error payload."""
        return False

    @classmethod
    def from_response(cls, response: Response) -> ClientRequestException:
        """Factory: parse error response, dispatch to the right exception type.

        Inspects the error payload once and returns the first matching subclass
        (e.g. ``DuplicatedObjectException``), so callers never deal with HTTP
        status codes or error JSON.
        """
        from office365.runtime import exceptions  # noqa: F401 — registers the built-in error types

        error = _parse_error(response)
        payload = _to_payload(error, response)
        exc: ClientRequestException = next(
            (exc_type(response=response) for exc_type in _ERROR_TYPES if exc_type.matches(payload)),
            cls(response=response),
        )

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


# Error types consulted by ``from_response`` (most specific first). The generic
# runtime types live in ``office365.runtime.exceptions`` and product packages
# (e.g. ``office365.sharepoint.exceptions``) register their own; both call
# ``register_error_type`` so the dispatcher stays product-agnostic.
_ERROR_TYPES: list[type[ClientRequestException]] = []


def register_error_type(exc_type: type[ClientRequestException]) -> None:
    """Register an error type for ``from_response`` dispatch.

    Modules call this at import time; the first matching type wins.
    """
    if exc_type not in _ERROR_TYPES:
        _ERROR_TYPES.insert(0, exc_type)


_LAZY_EXPORTS = ("DuplicatedObjectException", "ObjectNotFoundException")


def __getattr__(name: str):
    """Backward-compatible re-export of the generic error types (now in ``exceptions``)."""
    if name in _LAZY_EXPORTS:
        from office365.runtime import exceptions

        return getattr(exceptions, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
