"""Microsoft Teams throttling quotas (reference).

Teams evaluates four independent dimensions — **per app** (one client id across every
tenant), **per app per tenant**, **per resource** (a single team, channel or chat) and
**per user** — and a request is throttled by the first one it reaches. Rates are
requests per second, and each is a short burst window; a sustained workload is also
judged against a longer window at roughly 83% of the listed rate, so steady-state
traffic should sit below the number, not at it.

The rows below are the defaults, which cover any request a resource-specific table
does not name (`GET /teams/{id}`, `GET .../channels`, channel messages and chats are
called out because they are what this library is used for). A dash in the published
table means no dedicated limit for that dimension — the row is simply absent here.

Reference-only: the library reacts to the server signals
(:mod:`office365.runtime.http.throttling`) and retries with backoff.

Source: https://learn.microsoft.com/en-us/graph/throttling-limits#microsoft-teams-service-limits
"""

from __future__ import annotations

from typing import Tuple

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits#microsoft-teams-service-limits"
_SUPPORTED = LimitKind.SUPPORTED

#: The published table's four columns, in order.
_SCOPES = ("app", "app+tenant", "team, channel or chat", "user")

#: Default row per request type: (request_type, per-app, per-app-per-tenant, per-resource, per-user).
_DEFAULT_ROWS = (
    ("read", 1_500, 30, 1, 1),
    ("write", 300, 30, 1, 1),
    ("delete", 150, 15, 1, 1),
)

_DEFAULTS = tuple(
    Limit(
        "microsoft teams",
        value,
        _SUPPORTED,
        "requests",
        scope,
        note="default — any request a resource table does not name",
        doc=_DOC,
        window_seconds=1,
        request_type=request_type,
    )
    for request_type, *values in _DEFAULT_ROWS
    for scope, value in zip(_SCOPES, values)
)


def _rows(operation: str, *dimensions: Tuple[str, int]) -> Tuple[Limit, ...]:
    """The published rows of one operation, as ``(dimension, requests per second)`` pairs.

    Grouped by operation because the operation *is* the resource a request is counted
    against: a model binds the group for the call it makes. The table names a dimension
    only where it overrides the default, which is why a group is shorter than ``_SCOPES``.
    """
    return tuple(
        Limit(
            "microsoft teams",
            rate,
            _SUPPORTED,
            "requests",
            dimension,
            note=operation,
            doc=_DOC,
            window_seconds=1,
            request_type="read" if operation.startswith("GET") else "write",
        )
        for dimension, rate in dimensions
    )


#: One group per published operation, in the table's order. A model binds the rows of the
#: call it makes; the member that names an endpoint binds both its read and write rows.
TEAM_READ = _rows("GET /teams/{id}", ("app", 1_500), ("app+tenant", 30), ("team, channel or chat", 4))
TEAM_CHANNELS = _rows("GET /teams/{id}/channels", ("app", 1_200), ("app+tenant", 60), ("team, channel or chat", 4))
CHANNEL_MESSAGES_READ = _rows(
    "GET /teams/{id}/channels/{id}/messages", ("app", 200), ("app+tenant", 20), ("team, channel or chat", 1)
)
CHANNEL_MESSAGES_WRITE = _rows(
    "POST /teams/{id}/channels/{id}/messages",
    ("app", 500),
    ("app+tenant", 50),
    ("team, channel or chat", 1),
    ("user", 1),
)
CHAT_MESSAGES_READ = _rows("GET /chats/{id}/messages", ("app", 200), ("app+tenant", 20), ("team, channel or chat", 1))
CHAT_MESSAGES_WRITE = _rows(
    "POST /chats/{id}/messages", ("app", 200), ("app+tenant", 20), ("team, channel or chat", 1), ("user", 1)
)

#: The published table: the defaults no operation overrides, then every named operation.
TEAMS_QUOTAS = (
    _DEFAULTS
    + TEAM_READ
    + TEAM_CHANNELS
    + CHANNEL_MESSAGES_READ
    + CHANNEL_MESSAGES_WRITE
    + CHAT_MESSAGES_READ
    + CHAT_MESSAGES_WRITE
)

register_catalog(TEAMS_QUOTAS, product="teams")
