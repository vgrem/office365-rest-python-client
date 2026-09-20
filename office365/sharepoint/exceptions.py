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
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD, SAFE_PAGE_SIZE


class SecurityValidationException(ClientRequestException):
    """Raised when SharePoint rejects an expired/invalid form digest (HTTP 403)."""

    _CODES = ("-2130575251",)
    _MARKERS = ("security validation",)

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        return any(marker in payload.code for marker in cls._CODES) or any(
            marker in payload.message.lower() for marker in cls._MARKERS
        )


class SPQueryThrottledException(ClientRequestException):
    """Raised when a query exceeds the SharePoint **list view threshold**.

    SharePoint blocks (HTTP 500) queries that filter or sort on a **non-indexed**
    column and would scan/return more than the threshold (5,000 items by default),
    and sometimes single-shot collection loads of a large collection. See
    https://learn.microsoft.com/en-us/microsoft-365/community/how-to-handle-list-view-threshold

    The message is localized, so classification keys off the stable error code
    (``-2147024860``), with an English message marker as a fallback.
    """

    _CODES = ("-2147024860",)
    _MARKERS = ("list view threshold", "umbral de vista de lista")

    GUIDANCE = (
        f"This exceeds the SharePoint list view threshold ({LIST_VIEW_THRESHOLD:,} items by default). "
        f"To fix it, either: (1) page through the data with get_all(page_size<={SAFE_PAGE_SIZE}) "
        "(for list items) or Folder.get_files() / List.get_items(query, page_size=...); "
        "(2) filter/sort on an indexed column - add one with List.ensure_indexed('Column'); "
        "or (3) filter on ID (always indexed)."
    )

    @classmethod
    def matches(cls, payload: ErrorPayload) -> bool:
        return any(code in payload.code for code in cls._CODES) or any(
            marker in payload.message.lower() for marker in cls._MARKERS
        )

    def __str__(self) -> str:
        return f"{super().__str__()}\n{self.GUIDANCE}"


register_error_type(SecurityValidationException)
register_error_type(SPQueryThrottledException)
