"""Transport decorator that paces requests through a shared rate limiter.

Wraps any :class:`~office365.runtime.transport.base.BaseTransport` so every
request is gated by a shared :class:`~office365.runtime.http.throttling.RateLimiter`
before it is sent and every response (or error's response) is fed back into it.
The wrapper is transport-agnostic — it composes with ``requests`` today and with
an async transport later, and it keeps the pacing at the single I/O boundary so
call sites stay free of side effects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from office365.runtime.http.throttling import paced
from office365.runtime.transport.base import BaseTransport

if TYPE_CHECKING:
    from requests import Response

    from office365.runtime.http.request_options import RequestOptions
    from office365.runtime.http.throttling import RateLimiter


class ThrottledTransport(BaseTransport):
    """Decorates a transport with fleet-wide pacing from a shared limiter.

    Args:
        inner: The wrapped transport performing the actual I/O.
        limiter: The shared :class:`RateLimiter` gating the fleet.
    """

    def __init__(self, inner: BaseTransport, limiter: "RateLimiter") -> None:
        self._inner = inner
        self._limiter = limiter

    @property
    def inner(self) -> BaseTransport:
        """The wrapped transport."""
        return self._inner

    @property
    def limiter(self) -> "RateLimiter":
        """The shared rate limiter."""
        return self._limiter

    def execute(self, request: "RequestOptions") -> "Response":
        return paced(lambda: self._inner.execute(request), self._limiter)

    @property
    def proxies(self) -> dict[str, str] | None:
        return self._inner.proxies

    @property
    def verify(self) -> bool | str:
        return self._inner.verify

    @property
    def timeout(self) -> int | Tuple[int, int] | None:
        return self._inner.timeout

    def close(self) -> None:
        self._inner.close()
