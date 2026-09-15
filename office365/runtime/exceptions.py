"""Generic runtime request exceptions.

Concrete error types shared across products (Graph, SharePoint, ...). They
self-register with the dispatcher in
:mod:`office365.runtime.client_request_exception`, which imports this module
lazily so classification works regardless of import order.
"""

from __future__ import annotations

from office365.runtime.client_request_exception import (
    ClientRequestException,
    ErrorPayload,
    register_error_type,
)


class DuplicatedObjectException(ClientRequestException):
    """Raised when creating an object that already exists (HTTP 400 + ConflictingObjects)."""

    _CODES = frozenset({"nameAlreadyExists", "ErrorFolderExists", "-2130575342"})

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        return (
            payload.code in cls._CODES
            or any(detail.get("code") == "ConflictingObjects" for detail in payload.details)
            or "already exists" in payload.message.lower()
        )


class ObjectNotFoundException(ClientRequestException):
    """Raised when a requested object is not found (HTTP 404 or ResourceNotFound code)."""

    _CODES = frozenset({"itemnotfound", "resourcenotfound", "notfound"})

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        return "-2147024809" in payload.code or payload.code.lower() in cls._CODES


register_error_type(DuplicatedObjectException)
register_error_type(ObjectNotFoundException)
