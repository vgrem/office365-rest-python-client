"""Default HTTP transport backed by ``requests.Session``."""

from __future__ import annotations

from typing import Any, Optional, Tuple

from requests import Response, Session

from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import (
    DEFAULT_CONNECT_TIMEOUT,
    BaseTransport,
    NoTimeoutType,
    TimeoutValue,
)

#: Default timeout applied when none is configured: bounds the connect phase
#: (10 s) while leaving the read phase unbounded, so long streamed
#: uploads/downloads are unaffected. Pass
#: :data:`~office365.runtime.transport.base.NO_TIMEOUT` to disable it.
DEFAULT_TIMEOUT: Optional[Tuple[float, Optional[float]]] = (DEFAULT_CONNECT_TIMEOUT, None)


class RequestsTransport(BaseTransport):
    """HTTP transport using ``requests.Session`` for connection reuse.

    Args:
        session: Optional external ``Session`` for custom adapters or TLS config
        proxies: Transport-level proxy configuration applied to all requests
        verify: SSL verification (``True``, ``False``, or a CA bundle path)
        timeout: Request timeout — a number or a ``(connect, read)`` tuple. When
            ``None`` the :data:`DEFAULT_TIMEOUT` (10 s connect, unbounded read)
            applies; pass ``NO_TIMEOUT`` to disable timeouts entirely.
    """

    def __init__(
        self,
        session: Session | None = None,
        proxies: dict[str, str] | None = None,
        verify: bool | str = True,
        timeout: TimeoutValue | NoTimeoutType | None = None,
    ) -> None:
        self._session = session or Session()
        self._proxies = proxies
        self._verify = verify
        self._timeout = self._resolve_timeout(timeout)

    @staticmethod
    def _resolve_timeout(timeout: TimeoutValue | NoTimeoutType | None) -> Optional[TimeoutValue]:
        if timeout is None:
            return DEFAULT_TIMEOUT
        if isinstance(timeout, NoTimeoutType):
            return None
        return timeout

    @property
    def proxies(self) -> dict[str, str] | None:
        return self._proxies

    @property
    def verify(self) -> bool | str:
        return self._verify

    @property
    def timeout(self) -> Optional[TimeoutValue]:
        return self._timeout

    @property
    def auth(self) -> Any | None:
        return self._session.auth

    def execute(self, request: RequestOptions) -> Response:
        kwargs: dict[str, Any] = {"headers": request.headers}
        if request.verify is not None:
            kwargs["verify"] = request.verify
        if request.proxies is not None:
            kwargs["proxies"] = request.proxies
        if request.auth is not None:
            kwargs["auth"] = request.auth
        # A per-request timeout wins over the transport-level one; both accept a
        # single value or a ``(connect, read)`` tuple. When neither is set the
        # transport default (connect-bounded, read-unbounded) applies.
        timeout = request.timeout if request.timeout is not None else self._timeout
        if timeout is not None:
            kwargs["timeout"] = timeout

        method = request.method.value.lower()
        if method in ("post", "patch"):
            kwargs["data" if request.is_bytes or request.is_file else "json"] = request.data
        elif method == "put":
            kwargs["data"] = request.data
        elif method == "get":
            kwargs["stream"] = request.stream

        return getattr(self._session, method)(request.url, **kwargs)

    def reset_connections(self) -> None:
        """Clear the session's connection pools so the retry opens a new socket.

        ``Session.close()`` releases pooled (idle) connections while leaving the
        session usable, so the next request transparently builds a fresh pool.
        """
        self._session.close()

    def close(self) -> None:
        self._session.close()
