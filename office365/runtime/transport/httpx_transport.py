"""Optional native-async HTTP transport backed by ``httpx`` (encode/httpx).

Unlike the default :class:`~office365.runtime.transport.base.BaseTransport`
implementation — which offloads the blocking ``requests`` call to a worker
thread — this transport performs genuinely asynchronous I/O on the event loop.

It is **optional**: install it with ``pip install
office365-rest-python-client[httpx]`` and opt in per request via
:meth:`~office365.runtime.client_request.ClientRequest.with_async_transport`::

    from office365.runtime.transport.httpx_transport import HttpxTransport

    ctx = ClientContext(site_url).with_credentials(credentials)
    ctx.pending_request().with_async_transport(HttpxTransport())
    await ctx.web.get().execute_query_async()

The synchronous path keeps using the default ``requests``-based transport, so
adding this does not change existing behaviour.

Notes:
    * Responses are adapted to :class:`requests.Response` so downstream
      processing is unchanged; the body is read eagerly, so ``stream=True``
      downloads (``response.iter_content``) work but are buffered in memory.
    * TLS verification, proxies and redirect policy are client-level
      (constructor) settings; per-request ``verify``/``proxies`` are not honored.
"""

from __future__ import annotations

from typing import Any, Optional

from requests import Response
from requests.structures import CaseInsensitiveDict

from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import BaseTransport


class HttpxTransport(BaseTransport):
    """Native-async HTTP transport using ``httpx`` clients.

    Args:
        verify: TLS verification (``True``, ``False`` or a CA bundle path),
            applied to both clients.
        timeout: Default timeout in seconds (``None`` disables it, matching the
            default ``requests`` transport). A per-request timeout overrides it.
        follow_redirects: Whether to follow redirects (default ``True`` to match
            ``requests``).
        client: Optional pre-built ``httpx.Client`` (mainly for tests).
        async_client: Optional pre-built ``httpx.AsyncClient`` (mainly for tests).
        **client_kwargs: Extra keyword arguments forwarded to both clients.
    """

    def __init__(
        self,
        *,
        verify: bool | str = True,
        timeout: Optional[float] = None,
        follow_redirects: bool = True,
        client: Any | None = None,
        async_client: Any | None = None,
        **client_kwargs: Any,
    ) -> None:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise ImportError(
                "HttpxTransport requires httpx. Install it with 'pip install office365-rest-python-client[httpx]'."
            ) from exc

        self._httpx = httpx
        self._client = (
            client
            if client is not None
            else httpx.Client(verify=verify, timeout=timeout, follow_redirects=follow_redirects, **client_kwargs)
        )
        self._async_client = (
            async_client
            if async_client is not None
            else httpx.AsyncClient(verify=verify, timeout=timeout, follow_redirects=follow_redirects, **client_kwargs)
        )

    def execute(self, request: RequestOptions) -> Response:
        """Send a request synchronously through an ``httpx.Client``."""
        httpx_response = self._client.request(request.method.value, request.url, **self._build_kwargs(request))
        return self._to_requests_response(httpx_response)

    async def execute_async(self, request: RequestOptions) -> Response:
        """Send a request asynchronously through an ``httpx.AsyncClient``."""
        httpx_response = await self._async_client.request(
            request.method.value, request.url, **self._build_kwargs(request)
        )
        return self._to_requests_response(httpx_response)

    def close(self) -> None:
        """Close the synchronous client."""
        self._client.close()

    async def aclose(self) -> None:
        """Close both clients (the async one is awaited)."""
        await self._async_client.aclose()
        self._client.close()

    def _build_kwargs(self, request: RequestOptions) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"headers": request.headers}
        if request.auth is not None:
            kwargs["auth"] = request.auth
        if request.timeout is not None:
            kwargs["timeout"] = request.timeout

        method = request.method.value.lower()
        if method in ("post", "patch"):
            if request.data is not None:
                kwargs["content" if request.is_bytes or request.is_file else "json"] = request.data
        elif method == "put" and request.data is not None:
            kwargs["content"] = request.data
        return kwargs

    @staticmethod
    def _to_requests_response(httpx_response: Any) -> Response:
        """Adapt an ``httpx.Response`` to a ``requests.Response``.

        The body is materialised so ``content``/``json``/``iter_content`` behave
        exactly as on a ``requests`` response.
        """
        response = Response()
        response.status_code = httpx_response.status_code
        response.reason = httpx_response.reason_phrase
        response.url = str(httpx_response.url)
        response.headers = CaseInsensitiveDict(httpx_response.headers)
        if httpx_response.encoding is None:
            response.encoding = httpx_response.charset_encoding
        else:
            response.encoding = httpx_response.encoding
        response._content = httpx_response.content
        response._content_consumed = True  # type: ignore[reportAttributeAccessIssue]
        return response
