"""OneNote service throttling quotas (reference).

OneNote is the one Graph product whose limits differ by *context* rather than by
resource: a delegated call is counted per app per user (120 a minute, 400 an hour, five
at a time) and an app-only call per app (240 a minute, 800 an hour, twenty at a time).
Both columns apply to the same seven resources, so a model that declares them declares
both — which one is spent depends on the token, not on the type.

Reference-only: the library reacts to the server signals
(:mod:`office365.runtime.http.throttling`). These resources do **not** return
``Retry-After`` on a 429 — an hourly budget that is spent stays spent until the hour
rolls over — so a caller pacing by the response header has to pace by the clock instead.

Source: https://learn.microsoft.com/en-us/graph/throttling-limits#onenote-service-limits
"""

from __future__ import annotations

from office365.runtime.limits import Limit, LimitKind, register_catalog

_DOC = "https://learn.microsoft.com/en-us/graph/throttling-limits#onenote-service-limits"
_SUPPORTED = LimitKind.SUPPORTED
_BOUNDARY = LimitKind.BOUNDARY


def _context(scope: str, minute: int, hour: int, concurrent: int) -> tuple:
    """One context's three rows: the rate, the hourly budget, the concurrency ceiling."""
    return (
        Limit(
            "onenote",
            minute,
            _SUPPORTED,
            "requests",
            scope,
            note="requests per minute",
            doc=_DOC,
            window_seconds=60,
        ),
        Limit(
            "onenote",
            hour,
            _SUPPORTED,
            "requests",
            scope,
            note="requests per hour",
            doc=_DOC,
            window_seconds=3_600,
        ),
        # A concurrency limit is a rate window of zero: "five at a time", not "five a minute".
        Limit(
            "onenote",
            concurrent,
            _BOUNDARY,
            "requests",
            scope,
            note="in flight at any moment",
            doc=_DOC,
            window_seconds=0,
        ),
    )


#: Delegated calls: counted per app per user.
ONENOTE_DELEGATED = _context("app+user", 120, 400, 5)

#: App-only calls: counted per app across every user it serves.
ONENOTE_APP_ONLY = _context("app", 240, 800, 20)

ONENOTE_QUOTAS = ONENOTE_DELEGATED + ONENOTE_APP_ONLY

register_catalog(ONENOTE_QUOTAS, product="onenote")
