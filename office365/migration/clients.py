"""Configured clients for migration workloads.

A migration run is background work, and the service treats it as such. Microsoft
Graph throttles a low-priority request last (``x-ms-throttle-priority: low``) and
reports how close the tenant is to its limit on every response
(``x-ms-throttle-limit-percentage``). Sending the header and pacing on that
percentage are each one call on a client, and each is easy to leave out of an
export script — so they are bundled here, once.

Usage:

    >>> from office365.migration import migration_client
    >>> client = migration_client(GraphClient(tenant=tenant).with_client_secret(client_id, secret))
    >>> export = MailboxExport(client, ...)

The function configures the client it is given — every ``with_...`` in this
library does — so call it once, on a client the migration layer is about to use
exclusively, before the run starts. Calling it twice re-installs the pacing
limiter, which discards that limiter's observations: there is deliberately no
"already configured" flag, because a hidden one would make a second, differently
argumented call silently ineffective.

Scope note: the priority header is Graph-only. A SharePoint ``ClientContext``
gets pacing and no header — SharePoint signals load with
``X-SharePointHealthScore``, which the same limiter already reads.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext

_ClientT = TypeVar("_ClientT", bound="ClientRuntimeContext")


def migration_client(
    client: _ClientT,
    *,
    priority: str = "low",
    pace: bool = True,
) -> _ClientT:
    """Apply the background-workload policy to ``client`` and return it.

    Two settings, both opt-in on the client and both off by default in the
    library because an interactive request wants neither:

    - **priority** — ``x-ms-throttle-priority`` on every request. ``"low"`` for
      a bulk export or import, ``"high"`` only for a request a user is waiting
      on. Pass ``None`` to leave the header off. Graph-only; ignored for a
      SharePoint context.
    - **pace** — a shared :class:`~office365.runtime.http.throttling.RateLimiter`
      on the context's transport, so a wide batch pauses on the server's own
      signal (``x-ms-throttle-limit-percentage`` for Graph,
      ``X-SharePointHealthScore`` for SharePoint) instead of discovering the
      limit through ``429``s. Counters stay observable through
      :class:`~office365.migration.ThrottleMonitor`, which can be attached to the
      same client.

    Args:
        client: The Graph or SharePoint context the migration layer will use.
        priority: ``"low"`` (default), ``"normal"``, ``"high"``, or ``None``.
        pace: Whether to install the shared rate limiter (default ``True``).

    Returns:
        The same client, configured — so it can be assigned in one expression.

    Raises:
        ValueError: When ``priority`` is not an accepted value (raised by
            ``GraphClient.with_throttle_priority``).
    """
    if pace:
        client.with_rate_limit()

    if priority is not None:
        # Local import: the client module imports every Graph service, and most
        # migration work never sends a Graph request.
        from office365.graph_client import GraphClient

        if isinstance(client, GraphClient):
            client.with_throttle_priority(priority)

    return client


__all__ = ["migration_client"]
