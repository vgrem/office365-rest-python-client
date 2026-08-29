"""Parsing and reacting to throttling / health signals on responses.

SharePoint Online reports server load via ``X-SharePointHealthScore`` on every
response and ``Retry-After`` on throttled (429/503) responses. Per the current
Microsoft guidance it does **not** return IETF ``RateLimit-*`` headers — those
are parsed defensively here in case a proxy or other source provides them.

Two ways to use it:

- Attach :func:`rate_limit_hook` per query (``after_execute(..., include_response=True)``)
  or to the request event handler for every response;
- Wrap a workload in :func:`throttle_guard` for a scoped, self-removing guard
  that hides the event plumbing entirely.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import astuple, dataclass
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional

from requests import Response

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext


@dataclass(frozen=True)
class ThrottleLimits:
    """Throttling state reported by the server on a successful response.

    Attributes:
        limit: Maximum requests permitted in the current window.
        remaining: Requests still permitted before throttling kicks in.
        reset: Seconds until the quota window resets.
        retry_after: Seconds the server asks us to wait (``Retry-After``).
        health_score: SharePoint health score (0-100), if reported.
    """

    limit: Optional[int] = None
    remaining: Optional[int] = None
    reset: Optional[int] = None
    retry_after: Optional[int] = None
    health_score: Optional[int] = None


def parse_throttling(response: Response) -> Optional[ThrottleLimits]:
    """Parse throttling / health headers from a response into a ``ThrottleLimits``.

    Returns ``None`` when the response carries none of the tracked headers
    (e.g. a Microsoft Graph response), so hooks can stay silent for other APIs.

    Args:
        response: The raw HTTP response.

    Returns:
        ThrottleLimits, or None when no tracked headers are present.
    """
    limits = ThrottleLimits(
        limit=_to_int(response.headers.get("RateLimit-Limit")),
        remaining=_to_int(response.headers.get("RateLimit-Remaining")),
        reset=_to_int(response.headers.get("RateLimit-Reset")),
        retry_after=_to_int(response.headers.get("Retry-After")),
        health_score=_to_int(response.headers.get("X-SharePointHealthScore")),
    )
    if any(value is not None for value in astuple(limits)):
        return limits
    return None


def rate_limit_hook(callback: Optional[Callable[[ThrottleLimits], None]] = None) -> Callable[[Response], None]:
    """Return an after-execute hook that reports parsed throttling / health state.

    The returned hook is compatible with ``after_execute`` (it expects the raw
    ``Response``). It fires ``callback`` only when the response carries any of
    the tracked headers — silent otherwise.

    Usage:
        >>> from office365.runtime.http.throttling import rate_limit_hook
        >>> items.get().after_execute(rate_limit_hook(my_callback), include_response=True).execute_query()
    """

    def _hook(response: Response) -> None:
        limits = parse_throttling(response)
        if limits is not None and callable(callback):
            callback(limits)

    return _hook


@contextmanager
def throttle_guard(
    context: "ClientRuntimeContext",
    on_limits: Optional[Callable[[ThrottleLimits], None]] = None,
) -> Iterator[None]:
    """Monitor throttling / health signals on every response within a scope.

    Attaches :func:`rate_limit_hook` to the request's ``afterExecute`` event
    handler on enter and removes it on exit, so the guard applies to every query
    executed inside the ``with`` block — no ``include_response`` plumbing needed.

    Args:
        context: The client context to monitor.
        on_limits: Optional callback invoked with parsed state per response
          (only when any of the tracked headers are present).

    Usage:
        >>> from office365.runtime.http.throttling import throttle_guard, ThrottleLimits
        >>> def pace(limits: ThrottleLimits) -> None:
        ...     if limits.remaining is not None and limits.remaining < 10:
        ...         time.sleep(limits.reset or 1)
        >>> with throttle_guard(ctx, on_limits=pace):
        ...     ctx.execute_query()
    """
    handler = context.pending_request().afterExecute
    hook = rate_limit_hook(on_limits)
    handler += hook
    try:
        yield
    finally:
        handler -= hook


def _to_int(value: Any) -> Optional[int]:
    """Parse a header value into an int, returning None when absent/invalid."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
