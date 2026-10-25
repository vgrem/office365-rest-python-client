"""Outlook service throttling quotas (reference).

The Outlook service applies its limits to **each app ID and mailbox combination** —
one app reading one user or group mailbox. Exceeding the limit for one mailbox does
not affect the same app on another mailbox, which is why every row here is scoped
``app+mailbox``.

Reference-only: the library reacts to the server signals
(:mod:`office365.runtime.http.throttling` — ``Retry-After`` and the ``x-ms-throttle-*``
headers) and retries what the service says it will accept. It does not simulate the
per-mailbox token bucket, because a per-mailbox limit is not knowable from a single
request; a caller who wants to stay inside it bounds its own concurrency
(``ctx.execute_query_parallel(..., num_workers=4)``).

Source: https://learn.microsoft.com/en-us/graph/throttling-limits#outlook-service-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits#outlook-service-limits"
_SUPPORTED = LimitKind.SUPPORTED

#: The per-mailbox request budget, and the only one every Outlook endpoint spends. Declared
#: on ``OutlookItem`` (what messages, events and contacts share) and on ``OutlookUser`` (the
#: ``/outlook`` root): two hierarchies, one budget, so it is written on both rather than on a
#: single type neither of them inherits.
OUTLOOK_MAILBOX_BUDGETS = (
    Limit(
        "outlook",
        10_000,
        _SUPPORTED,
        "requests",
        "app+mailbox",
        note="v1.0 and beta endpoints",
        doc=_DOC,
        window_seconds=600,
    ),
    # A concurrency limit is a rate window of zero: "four at a time", not "four per period".
    Limit(
        "outlook",
        4,
        _SUPPORTED,
        "requests",
        "app+mailbox",
        note="in flight at any moment",
        doc=_DOC,
        window_seconds=0,
    ),
)

#: Attachment uploads (``PATCH``/``POST``/``PUT``) are counted against their own byte budget,
#: which is why it is declared on ``AttachmentCollection`` -- the one place a mailbox uploads.
OUTLOOK_UPLOAD = Limit(
    "outlook",
    150 * 1024 * 1024,
    _SUPPORTED,
    "bytes",
    "app+mailbox",
    note="upload (PATCH, POST, PUT)",
    doc=_DOC,
    window_seconds=300,
)

#: JSON batching: Graph feeds the Outlook service at most four sub-requests at a time unless
#: the batch uses ``dependsOn``, in which case it sends them one at a time. The cap is
#: Outlook's, so it rides the batch entry point and its note carries the qualification --
#: a batch that addresses other services is not bound by it.
OUTLOOK_BATCH = Limit(
    "outlook",
    4,
    _SUPPORTED,
    "requests",
    "batch",
    note="sub-requests in flight per JSON batch that addresses Outlook; dependsOn serializes them instead",
    doc=_DOC,
    window_seconds=0,
)

OUTLOOK_QUOTAS = (*OUTLOOK_MAILBOX_BUDGETS, OUTLOOK_UPLOAD, OUTLOOK_BATCH)

register_catalog(OUTLOOK_QUOTAS, product="outlook")
