"""Microsoft Graph throttling limits — a reference catalog.

Graph imposes a **global** limit (130,000 requests / 10 s per app across all
tenants) plus **service-specific** limits, evaluated per scope (per app, per
tenant, per app + tenant, per resource) and per request type (read / write /
any). The first limit reached triggers throttling: HTTP **429** with a
``Retry-After`` header.

These are :class:`~office365.runtime.limits.Limit` values (rate quotas) — the
same vocabulary used everywhere. They're **reference-only**: Graph throttling is
dynamic and server-signalled (``Retry-After``, ``x-ms-throttle-limit-percentage``,
``x-ms-resource-unit``), so the library *reacts* to the signals
(:mod:`office365.runtime.http.throttling`) rather than enforcing a static budget.
Bind a quota to the model with ``@limit(GraphLimits.X)`` (see ``GraphClient``).

Sources:

- https://learn.microsoft.com/en-us/graph/throttling
- https://learn.microsoft.com/en-us/graph/throttling-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits"
_SUPPORTED = LimitKind.SUPPORTED

# Scopes.
_APP = "app"  # per app across all tenants
_TENANT = "tenant"  # per tenant for all apps
_APP_TENANT = "app+tenant"  # per app per tenant
_RESOURCE = "resource"  # per resource (call record, mailbox, ...)
_USER = "user"


def _quota(
    name: str,
    value: int,
    window_seconds: int,
    scope: str = _APP_TENANT,
    request_type: str = "any",
    unit: str = "requests",
    note: str = "",
) -> Limit:
    return Limit(
        name,
        value,
        _SUPPORTED,
        unit,
        scope,
        note=note,
        doc=_DOC,
        window_seconds=window_seconds,
        request_type=request_type,
    )


class GraphLimits:
    """The Microsoft Graph throttling-limit catalog (reference-only).

    Iterate :meth:`catalog` to render the table; the attributes name the headline
    quotas. Graph is throttled per scope, so a service usually has several entries
    (``name`` is the service).
    """

    # --- Global -------------------------------------------------------------
    GLOBAL = _quota("global", 130_000, 10, _APP, note="any request type, across all tenants")

    # --- Identity and access (ResourceUnits, token bucket) ------------------
    IDENTITY_APP_TENANT = _quota(
        "identity",
        3_500,
        10,
        _APP_TENANT,
        unit="resource_units",
        note="small tenants (<50 users); 5,000 medium (50-500), 8,000 large (>500)",
    )
    #: Representative identity quota for ``@limit`` bindings (the app+tenant bucket).
    IDENTITY = IDENTITY_APP_TENANT
    IDENTITY_APP = _quota("identity", 150_000, 20, _APP, unit="resource_units")
    IDENTITY_WRITE = _quota("identity", 3_000, 150, _APP_TENANT, "write")
    IDENTITY_APP_WRITE = _quota("identity", 35_000, 300, _APP, "write")
    IDENTITY_TENANT_WRITE = _quota("identity", 18_000, 300, _TENANT, "write")

    # --- Identity and access reports ----------------------------------------
    IDENTITY_REPORTS_APP = _quota("identity reports", 122, 10, _APP)
    IDENTITY_REPORTS_APP_TENANT = _quota("identity reports", 5, 10, _APP_TENANT)
    SIGN_IN_ACTIVITY = _quota("identity reports", 10, 60, _APP_TENANT, note="GET signInActivity")

    # --- Identity device operations -----------------------------------------
    DEVICE_WRITE = _quota("identity devices", 3_000, 150, _APP_TENANT, "write")
    DEVICE_USER_WRITE = _quota("identity devices", 25, 10, _USER, "write")

    # --- Identity protection and conditional access -------------------------
    IDENTITY_PROTECTION = _quota("identity protection", 1, 1, _TENANT, note="no Retry-After header")

    # --- Identity providers -------------------------------------------------
    IDENTITY_PROVIDERS_TENANT = _quota("identity providers", 300, 60, _TENANT)
    IDENTITY_PROVIDERS_APP = _quota("identity providers", 200, 60, _APP_TENANT)

    # --- Identity data policy operations ------------------------------------
    DATA_POLICY = _quota("identity data policy", 10_000, 3600, _TENANT, note="no Retry-After header")

    # --- Assignment ---------------------------------------------------------
    ASSIGNMENT_APP_TENANT = _quota("assignment", 350, 10, _APP_TENANT)
    ASSIGNMENT_TENANT = _quota("assignment", 700, 10, _TENANT)

    # --- Bookings -----------------------------------------------------------
    BOOKINGS = _quota("bookings", 4, 0, _APP_TENANT, unit="concurrent", note="per app + booking mailbox")

    # --- Cloud communications -----------------------------------------------
    CALLS = _quota("cloud communications", 50_000, 15, _APP_TENANT, note="calls")
    PRESENCE = _quota("cloud communications", 10_000, 30, _APP_TENANT, note="presence")
    VIRTUAL_EVENT_GET = _quota("cloud communications", 750, 30, _APP, "read", note="virtual events")
    VIRTUAL_EVENT_WRITE = _quota("cloud communications", 15, 30, _APP, "write", note="virtual events")
    CALL_RECORDS_APP = _quota("call records", 15_000, 20, _APP)
    CALL_RECORDS_TENANT = _quota("call records", 10_000, 20, _TENANT)
    CALL_RECORDS_APP_TENANT = _quota("call records", 1_500, 20, _APP_TENANT)
    CALL_RECORD = _quota("call records", 40, 20, _RESOURCE, note="per call record")
    PSTN_CALL_RECORDS = _quota("call records (PSTN)", 1_000, 60, _TENANT)

    # --- Excel --------------------------------------------------------------
    EXCEL_APP = _quota("excel", 5_000, 10, _APP)
    EXCEL_APP_TENANT = _quota("excel", 1_500, 10, _APP_TENANT)

    # --- Education ----------------------------------------------------------
    EDUCATION_APP = _quota("education", 400_000, 20, _APP)
    EDUCATION_APP_TENANT = _quota("education", 35_000, 10, _APP_TENANT)

    # --- Exchange message trace ---------------------------------------------
    MESSAGE_TRACE = _quota("exchange message trace", 100, 300, _TENANT)

    # --- Insights -----------------------------------------------------------
    INSIGHTS = _quota("insights", 10_000, 600, _APP_TENANT, note="me/insights; 4 concurrent")

    # --- Information protection ---------------------------------------------
    INFORMATION_PROTECTION = _quota("information protection", 150, 900, _TENANT, "write")
    INFORMATION_PROTECTION_DAILY = _quota("information protection", 10_000, 86_400, _TENANT, "write")

    # --- Intune -------------------------------------------------------------
    INTUNE_WRITE_TENANT = _quota("intune", 200, 20, _TENANT, "write")
    INTUNE_WRITE_APP = _quota("intune", 100, 20, _APP_TENANT, "write")
    INTUNE_TENANT = _quota("intune", 2_000, 20, _TENANT)
    INTUNE_APP = _quota("intune", 1_000, 20, _APP_TENANT)

    @classmethod
    def catalog(cls) -> list[Limit]:
        """Every declared limit, ordered by definition (aliases de-duplicated)."""
        seen: set[int] = set()
        result: list[Limit] = []
        for value in vars(cls).values():
            if isinstance(value, Limit) and id(value) not in seen:
                seen.add(id(value))
                result.append(value)
        return result
