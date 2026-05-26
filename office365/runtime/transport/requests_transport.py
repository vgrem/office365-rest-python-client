"""Default HTTP transport backed by ``requests.Session``."""

from __future__ import annotations

from typing import Any, Tuple

from requests import Response, Session

from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import BaseTransport


class RequestsTransport(BaseTransport):
    """HTTP transport using ``requests.Session`` for connection reuse.

    Args:
        session: Optional external ``Session`` for custom adapters or TLS config
        proxies: Transport-level proxy configuration applied to all requests
        verify: SSL verification (``True``, ``False``, or a CA bundle path)
        timeout: Request timeout in seconds (applied when per-request timeout is not set)
    """

    def __init__(
        self,
        session: Session | None = None,
        proxies: dict[str, str] | None = None,
        verify: bool | str = True,
        timeout: int | Tuple[int, int] | None = None,
    ) -> None:
        self._session = session or Session()
        self._proxies = proxies
        self._verify = verify
        self._timeout = timeout

    @property
    def proxies(self) -> dict[str, str] | None:
        return self._proxies

    @property
    def verify(self) -> bool | str:
        return self._verify

    @property
    def timeout(self) -> int | Tuple[int, int] | None:
        return self._timeout

    def execute(self, request: RequestOptions) -> Response:
        kwargs: dict[str, Any] = {"headers": request.headers}
        if request.verify is not None:
            kwargs["verify"] = request.verify
        if request.proxies is not None:
            kwargs["proxies"] = request.proxies
        if request.auth is not None:
            kwargs["auth"] = request.auth

        method = request.method.value.lower()
        if method in ("post", "patch"):
            kwargs["data" if request.is_bytes or request.is_file else "json"] = request.data
        elif method == "put":
            kwargs["data"] = request.data
        elif method == "get":
            kwargs["stream"] = request.stream

        return getattr(self._session, method)(request.url, **kwargs)

    def close(self) -> None:
        self._session.close()
