"""Microsoft Graph cloud-communications throttling quotas (reference).

A row is bound where the request is made — the budget rows on the resource type,
a per-record ceiling on the navigation that reads that record's children, an
operation ceiling on the method that performs the operation:

===========================  =========================================
row                          declared on
===========================  =========================================
``CALL_QUOTAS``              ``Call``
``CALL_RECORD_BUDGETS``      ``CallRecord``
``CALL_RECORD_RESOURCE_QUOTA``  ``CallRecord.sessions`` / ``.participants_v2``
``CALL_RECORD_FEED_QUOTA``   ``CallRecordCollection``
``PSTN_RECORD_QUOTAS``       ``CallRecordCollection.get_direct_routing_calls``
``PRESENCE_QUOTAS``          ``Presence``
``VIRTUAL_EVENT_QUOTAS``     ``VirtualEvent``
===========================  =========================================

Reference-only — the library reacts to the server signals
(:mod:`office365.runtime.http.throttling`). The catalog registers itself at import, so
`office365.limits.catalog()` sees these rows.

Source: https://learn.microsoft.com/en-us/graph/throttling-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits"
_CALL_RECORD_DOC = f"{_DOC}#call-records-limits"
_PSTN_RECORD_DOC = f"{_DOC}#pstn-call-records-limits"
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

#: The budgets every call-record request spends from, whatever the endpoint. The
#: published table frames them as "the limits apply to the following *resources*:
#: callRecord, participant, session" — which is why they are declared on the resource
#: type (``CallRecord``) and not on one of its methods.
CALL_RECORD_BUDGETS = (
    Limit(
        "call records",
        15_000,
        _SUPPORTED,
        "requests",
        "app",
        note=("all tenants; callRecord, participant and session resources"),
        doc=_CALL_RECORD_DOC,
        window_seconds=20,
    ),
    Limit(
        "call records",
        10_000,
        _SUPPORTED,
        "requests",
        "tenant",
        note="all applications",
        doc=_CALL_RECORD_DOC,
        window_seconds=20,
    ),
    Limit(
        "call records",
        1_500,
        _SUPPORTED,
        "requests",
        "app+tenant",
        doc=_CALL_RECORD_DOC,
        window_seconds=20,
    ),
)

#: The per-resource budget: reading the sessions, participants or segments **of one call
#: record** is capped on its own. Declared on the navigations that read them
#: (``CallRecord.sessions`` / ``.participants_v2``), because a per-record budget is a
#: property of that record's children and of nothing else.
CALL_RECORD_RESOURCE_QUOTA = Limit(
    "call records",
    40,
    _SUPPORTED,
    "requests",
    "call record",
    note="sessions, participants and segments of one call record",
    doc=_CALL_RECORD_DOC,
    window_seconds=20,
)

#: A separate 40/20s ceiling for the operation that lists call records — same number as
#: the per-record row, different fact. Declared on the collection.
CALL_RECORD_FEED_QUOTA = Limit(
    "call records",
    40,
    _SUPPORTED,
    "requests",
    "collection",
    note="list call records",
    doc=_CALL_RECORD_DOC,
    window_seconds=20,
)

#: Every published call-record row. A view over the three groups above — the same row
#: objects, so registering it adds no second copy.
CALL_RECORD_QUOTAS = (*CALL_RECORD_BUDGETS, CALL_RECORD_RESOURCE_QUOTA, CALL_RECORD_FEED_QUOTA)

#: The PSTN log rows (``getDirectRoutingCalls`` and friends) have their own table and
#: their own ceiling *per collection* — the sharpest example of a quota that belongs to
#: one operation rather than to a resource type.
PSTN_RECORD_QUOTAS = (
    Limit(
        "PSTN call records",
        1_000,
        _SUPPORTED,
        "requests",
        "tenant",
        note="directRoutingLogRow, pstnCallLogRow, pstnBlockedUsersLogRow, smsLogRow",
        doc=_PSTN_RECORD_DOC,
        window_seconds=60,
    ),
    Limit(
        "PSTN call records",
        200,
        _SUPPORTED,
        "requests",
        "app+tenant",
        doc=_PSTN_RECORD_DOC,
        window_seconds=60,
    ),
    Limit(
        "PSTN call records",
        50,
        _SUPPORTED,
        "requests",
        "collection",
        note="per collection",
        doc=_PSTN_RECORD_DOC,
        window_seconds=60,
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
        note="virtual events; across all tenants",
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
        note="virtual events; across all tenants",
        doc=_DOC,
        window_seconds=30,
    ),
)

register_catalog(
    CALL_QUOTAS,
    CALL_RECORD_QUOTAS,
    PSTN_RECORD_QUOTAS,
    PRESENCE_QUOTAS,
    VIRTUAL_EVENT_QUOTAS,
    product="cloud-communications",
)
