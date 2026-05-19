"""Default HTTP transport backed by ``requests.Session``."""

from __future__ import annotations

from typing import Any

from requests import Response, Session

from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import BaseTransport


class RequestsTransport(BaseTransport):
    """HTTP transport using ``requests.Session`` for connection reuse.

    Accepts an optional external ``Session`` for users who need custom
    adapters, TLS configuration, or NTLM/SSPI support.
    """

    def __init__(self, session: Session | None = None) -> None:
        self._session = session or Session()

    def execute(self, request: RequestOptions) -> Response:
        kwargs = self._build_kwargs(request)
        method = request.method.value.lower()
        return getattr(self._session, method)(request.url, **kwargs)

    def close(self) -> None:
        self._session.close()

    def _build_kwargs(self, request: RequestOptions) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"headers": request.headers, "verify": request.verify}

        if request.auth is not None:
            kwargs["auth"] = request.auth
        if request.proxies is not None:
            kwargs["proxies"] = request.proxies
        if request.timeout is not None:
            kwargs["timeout"] = request.timeout

        if request.method in (HttpMethod.Post, HttpMethod.Patch):
            key = "data" if request.is_bytes or request.is_file else "json"
            kwargs[key] = request.data
        elif request.method == HttpMethod.Put:
            kwargs["data"] = request.data
        elif request.method == HttpMethod.Get:
            kwargs["stream"] = request.stream

        return kwargs
