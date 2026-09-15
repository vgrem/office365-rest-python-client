"""SharePoint-specific request exceptions.

These self-register with
:func:`~office365.runtime.client_request_exception.register_error_type` so the
product-agnostic dispatcher in the runtime can classify SharePoint error
responses without importing this package.
"""

from __future__ import annotations

from office365.runtime.client_request_exception import (
    ClientRequestException,
    ErrorPayload,
    register_error_type,
)


class SecurityValidationException(ClientRequestException):
    """Raised when SharePoint rejects an expired/invalid form digest (HTTP 403)."""

    _CODES = ("-2130575251",)
    _MARKERS = ("security validation",)

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        return any(marker in payload.code for marker in cls._CODES) or any(
            marker in payload.message.lower() for marker in cls._MARKERS
        )


register_error_type(SecurityValidationException)
