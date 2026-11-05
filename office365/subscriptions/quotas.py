"""Microsoft Graph change-notification subscription throttling quotas (reference).

Every subscription request is counted twice — once against the app across all its
tenants and once against the app inside the tenant it addresses — and the second is the
smaller by an order of magnitude. A migration that renews thousands of subscriptions
per tenant runs into the per-tenant column, not the per-app one, which is why both are
written here rather than only the stricter.

Reference-only: the library reacts to the server signals
(:mod:`office365.runtime.http.throttling` — ``Retry-After`` and ``x-ms-throttle-*``) and
retries with backoff. It does not model the bucket.

Source: https://learn.microsoft.com/en-us/graph/throttling-limits#subscription-service-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits#subscription-service-limits"
_SUPPORTED = LimitKind.SUPPORTED

#: One group per published row, in the table's order. The publish table names
#: ``(per app for all tenants, per app per tenant)`` for each, so each group is two rows.
SUBSCRIPTION_CHANGES = (
    Limit(
        "subscription change",
        2_000,
        _SUPPORTED,
        "requests",
        "app",
        note="POST, PUT, DELETE, PATCH",
        doc=_DOC,
        window_seconds=20,
        request_type="write",
    ),
    Limit(
        "subscription change",
        500,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="POST, PUT, DELETE, PATCH",
        doc=_DOC,
        window_seconds=20,
        request_type="write",
    ),
)

SUBSCRIPTION_REAUTHORIZE = (
    Limit(
        "subscription reauthorize",
        4_000,
        _SUPPORTED,
        "requests",
        "app",
        note="POST /subscriptions/{id}/reauthorize",
        doc=_DOC,
        window_seconds=20,
        request_type="write",
    ),
    Limit(
        "subscription reauthorize",
        1_000,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="POST /subscriptions/{id}/reauthorize",
        doc=_DOC,
        window_seconds=20,
        request_type="write",
    ),
)

SUBSCRIPTION_READ = (
    Limit(
        "subscription",
        2_000,
        _SUPPORTED,
        "requests",
        "app",
        note="GET /subscriptions/{id}",
        doc=_DOC,
        window_seconds=20,
        request_type="read",
    ),
    Limit(
        "subscription",
        500,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="GET /subscriptions/{id}",
        doc=_DOC,
        window_seconds=20,
        request_type="read",
    ),
)

#: The list call is the narrow one: 40 requests per 20 seconds for every tenant the app
#: serves, so a caller enumerating subscriptions across tenants has almost no headroom.
SUBSCRIPTION_LIST = (
    Limit(
        "subscription list",
        40,
        _SUPPORTED,
        "requests",
        "app",
        note="GET /subscriptions",
        doc=_DOC,
        window_seconds=20,
        request_type="read",
    ),
    Limit(
        "subscription list",
        25,
        _SUPPORTED,
        "requests",
        "app+tenant",
        note="GET /subscriptions",
        doc=_DOC,
        window_seconds=20,
        request_type="read",
    ),
)

SUBSCRIPTION_QUOTAS = SUBSCRIPTION_CHANGES + SUBSCRIPTION_REAUTHORIZE + SUBSCRIPTION_READ + SUBSCRIPTION_LIST

register_catalog(SUBSCRIPTION_QUOTAS, product="subscriptions")
