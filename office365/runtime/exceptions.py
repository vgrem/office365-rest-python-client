"""Generic runtime request exceptions.

Concrete error types shared across products (Graph, SharePoint, ...). They
self-register with the dispatcher in
:mod:`office365.runtime.client_request_exception`, which imports this module
lazily so classification works regardless of import order.
"""

from __future__ import annotations

import re
from typing import Optional

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


class FileLockedException(ClientRequestException):
    """Raised when a file is locked and the requested change is rejected (HTTP 423).

    The usual cause is a **shared lock**: the file is open for coauthoring in
    Office (web or desktop), so SharePoint/Graph refuses the write. Unlike a
    check-out lock, a shared lock cannot be broken through the API. See
    :attr:`GUIDANCE` for the available options.
    """

    _CODES = ("-2147018894", "spfilelockexception", "resourcelocked")
    _MARKERS = ("locked for shared use", "resource is locked", "file is locked")

    GUIDANCE = (
        "The file is locked - typically because it is open for editing in Office. A shared lock "
        "cannot be broken through the API. Either retry until the other session closes "
        "(execute_query_retry(is_retriable=retry_on(FileLockedException))), update metadata only "
        "with ListItem.update_ex(bypass_shared_lock=True), or - for delete - pass "
        "bypass_shared_lock=True. The lock holder is available via .lock_owner."
    )

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        if payload.status == 423:  # noqa: PLR2004
            return True
        code = payload.code.lower()
        if any(marker in code for marker in cls._CODES):
            return True
        return any(marker in payload.message.lower() for marker in cls._MARKERS)

    @property
    def lock_owner(self) -> Optional[str]:
        """Best-effort display name of the user holding the lock (parsed from the message)."""
        match = re.search(r"locked for shared use by (.+?)\s*\[", self.message, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def __str__(self) -> str:
        owner = self.lock_owner
        described = f"{super().__str__()} (locked by {owner})" if owner else super().__str__()
        return f"{described}\n{self.GUIDANCE}"


register_error_type(FileLockedException)
