"""Parsing and reacting to throttling / health signals on responses.

SharePoint Online reports server load via ``X-SharePointHealthScore`` on every
response and ``Retry-After`` on throttled (429/503) responses. Per the current
Microsoft guidance it does **not** return IETF ``RateLimit-*`` headers — those
are parsed defensively here in case a proxy or other source provides them.

Two distinct concerns live here:

**Control** — act on the signals to pace the fleet. :class:`RateLimiter` +
:func:`paced` (used by ``ThrottledTransport``) gate every send and observe every
response, including failures, without touching error propagation. This is the
mature pipeline/transport-policy pattern (Azure ``RetryPolicy``, botocore
adaptive mode, urllib3 ``Retry``).

**Observability** — report the signals to the caller. :func:`rate_limit_hook`
and :func:`throttle_guard` attach to the request's ``afterExecute`` event and
never change control flow. Use these when you only want to *know* about
throttling; use the limiter when you want to *act* on it.

Note: request ``onError`` handlers mark an error as handled (they swallow it —
see :meth:`ClientRequest.on_error`), so they must not be used for observation.
"""

from __future__ import annotations

import threading
import time
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

    Observation only — it never changes control flow (unlike :class:`RateLimiter`).
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


@dataclass(frozen=True)
class PaceState:
    """The group gate: a monotonic deadline before which requests must wait.

    Produced only by :func:`pace` (pure) so the pacing policy is trivially
    testable without a clock, a lock, or a sleep.
    """

    next_available_at: float = 0.0


def pace(
    state: PaceState,
    limits: Optional[ThrottleLimits],
    *,
    now: float,
    health_threshold: int = 80,
    min_interval: float = 0.0,
) -> PaceState:
    """Pure transition: observed server limits -> next gate state.

    A ``Retry-After`` gates the fleet for that long; a high
    ``X-SharePointHealthScore`` applies a short, scaled pace so the group eases
    off as the farm heats up. Returns ``state`` unchanged when nothing applies.

    Args:
        state: The current gate state.
        limits: Parsed throttling/health signals (or ``None``).
        now: Monotonic "now" (injected — the function reads no clock).
        health_threshold: Health score at/above which the group paces.
        min_interval: Minimum pause applied on a high health score.
    """
    if limits is None:
        return state
    delay = 0.0
    if limits.retry_after is not None and limits.retry_after > 0:
        delay = max(delay, float(limits.retry_after))
    if limits.health_score is not None and limits.health_score >= health_threshold:
        delay = max(delay, (limits.health_score - health_threshold) / 20.0, min_interval)
    if delay <= 0:
        return state
    return PaceState(max(state.next_available_at, now + delay))


def wait_delay(state: PaceState, *, now: float) -> float:
    """Pure: seconds until the gate opens (``0`` when already open)."""
    return max(0.0, state.next_available_at - now)


def paced(func: Callable[[], Response], gate: "RateLimiter") -> Response:
    """Run ``func`` under a shared rate limiter — the functional guard.

    Mirrors :func:`~office365.runtime.retry.retry`: it waits for the group gate,
    then feeds the outcome (returned response or ``exception.response``) back to
    the limiter. No call-site side effects; composable and thread-safe.

    Args:
        func: Callable performing one request/operation.
        gate: The shared :class:`RateLimiter` to pace against.
    """
    gate.acquire()
    try:
        result = func()
    except Exception as ex:
        gate.observe(getattr(ex, "response", None))
        raise
    gate.observe(result)
    return result


class RateLimiter:
    """Thread-safe gate shared across workers so parallel requests pace as a group.

    Unlike :func:`throttle_guard` (reactive, per-context) and the per-request
    backoff in ``retry.py``, this limiter coordinates a *fleet* of clones/workers:
    before any request is sent it blocks until the group gate is open, and when
    any worker observes throttling it pauses the whole group.

    The pacing policy lives in the pure :func:`pace` / :func:`wait_delay`; this
    class is only the thread-safe state holder with injectable ``clock`` and
    ``sleep`` (so tests can run without real time). Opt-in — wrap a transport
    with :class:`~office365.runtime.transport.throttled_transport.ThrottledTransport`
    or attach it to a context with :meth:`bind`; the existing per-request retry
    remains as the safety net.
    """

    _SLEEP_GRANULARITY = 0.05

    def __init__(
        self,
        health_threshold: int = 80,
        min_interval: float = 0.0,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._lock = threading.Lock()
        self._state = PaceState()
        self._health_threshold = health_threshold
        self._min_interval = min_interval
        self._clock = clock
        self._sleep = sleep

    def snapshot(self) -> PaceState:
        """Return the current gate state (a pure value)."""
        with self._lock:
            return self._state

    def acquire(self) -> None:
        """Block the calling thread until the group gate opens.

        Called before a request is sent; safe to invoke from many threads.
        """
        while True:
            with self._lock:
                wait = wait_delay(self._state, now=self._clock())
            if wait <= 0:
                return
            self._sleep(min(wait, self._SLEEP_GRANULARITY))

    def observe(self, response: Optional[Response]) -> None:
        """Record throttling signals and pause the group when the server asks."""
        if response is None:
            return
        limits = parse_throttling(response)
        if limits is None:
            return
        with self._lock:
            self._state = pace(
                self._state,
                limits,
                now=self._clock(),
                health_threshold=self._health_threshold,
                min_interval=self._min_interval,
            )

    def bind(self, context: "ClientRuntimeContext") -> "RateLimiter":
        """Pace every request of a context (or ``clone``) by wrapping its transport.

        Delegates to :meth:`ClientRequest.with_rate_limiter` on the context's
        request, so the shared limiter gates each send and observes each response
        (and any error's ``response``).

        Args:
            context: The client context to gate.
        """
        context.pending_request().with_rate_limiter(self)
        return self

    def reset(self) -> None:
        """Clear the current gate (used by tests / recovery)."""
        with self._lock:
            self._state = PaceState()
