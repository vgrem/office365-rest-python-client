"""Microsoft Graph cloud-communications throttling quotas (reference).

Declared on the model with ``@limit(*CALL_QUOTAS)`` etc. (see ``Call``,
``Presence``, ``VirtualEvent``). Reference-only — the library reacts to the
server signals (:mod:`office365.runtime.http.throttling`).

Source: https://learn.microsoft.com/en-us/graph/throttling-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits"
_SUPPORTED = LimitKind.SUPPORTED

CALL_QUOTAS = (
    Limit(
        "cloud communications",
        50_000,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="calls",
        doc=_DOC,
        window_seconds=15,
    ),
)

PRESENCE_QUOTAS = (
    Limit(
        "cloud communications",
        10_000,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="presence",
        doc=_DOC,
        window_seconds=30,
    ),
)

VIRTUAL_EVENT_QUOTAS = (
    Limit(
        "cloud communications",
        750,
        _SUPPORTED,
        "requests",
        "app",
        request_type="read",
        note="virtual events",
        doc=_DOC,
        window_seconds=30,
    ),
    Limit(
        "cloud communications",
        15,
        _SUPPORTED,
        "requests",
        "app",
        request_type="write",
        note="virtual events",
        doc=_DOC,
        window_seconds=30,
    ),
)
