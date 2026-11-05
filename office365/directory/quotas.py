"""Microsoft Graph identity throttling quotas (reference).

Declared on the model with ``@limit(*IDENTITY_QUOTAS)`` (see ``DirectoryObject``,
``SubscribedSku``, ``Domain``) — Graph throttles the identity API surface with a
**ResourceUnits** token bucket plus write quotas. Reference-only: the library
reacts to the server signals (:mod:`office365.runtime.http.throttling`). The catalog
registers itself at import, so `office365.limits.catalog()` sees these rows.

Source: https://learn.microsoft.com/en-us/graph/throttling-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits"
_SUPPORTED = LimitKind.SUPPORTED

#: Identity and access quotas (the whole `/users`, `/groups`, ... surface).
IDENTITY_QUOTAS = (
    Limit(
        "identity",
        3_500,
        _SUPPORTED,
        "resource_units",
        "app+tenant",
        note="small tenants (<50 users); 5,000 medium (50-500), 8,000 large (>500)",
        doc=_DOC,
        window_seconds=10,
    ),
    Limit("identity", 150_000, _SUPPORTED, "resource_units", "app", doc=_DOC, window_seconds=20),
    Limit("identity", 3_000, _SUPPORTED, "requests", "app+tenant", doc=_DOC, window_seconds=150, request_type="write"),
    Limit("identity", 35_000, _SUPPORTED, "requests", "app", doc=_DOC, window_seconds=300, request_type="write"),
    Limit("identity", 18_000, _SUPPORTED, "requests", "tenant", doc=_DOC, window_seconds=300, request_type="write"),
)

#: Invitations are counted against the tenant for all apps, not per app: 150 requests
#: every 5 seconds, whatever the client id. A tenant-wide invitation sweep spends the
#: same budget the Entra portal does.
INVITATION_QUOTAS = (
    Limit(
        "invitations",
        150,
        _SUPPORTED,
        "requests",
        "tenant",
        note="any operation on /invitations, all apps",
        doc=_DOC,
        window_seconds=5,
        request_type="any",
    ),
)

#: The identity-protection and conditional-access surface answers one request a second
#: for the whole tenant, and a 429 comes back with no ``Retry-After``: a caller that
#: retries on the header alone retries immediately, forever.
IDENTITY_PROTECTION_QUOTAS = (
    Limit(
        "identity protection and conditional access",
        1,
        _SUPPORTED,
        "requests",
        "tenant",
        note="riskDetection, namedLocation, conditionalAccessPolicy — no Retry-After on 429",
        doc=_DOC,
        window_seconds=1,
        request_type="any",
    ),
)

register_catalog(IDENTITY_QUOTAS, INVITATION_QUOTAS, IDENTITY_PROTECTION_QUOTAS, product="directory")
