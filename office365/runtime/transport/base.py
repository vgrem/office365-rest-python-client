"""Pluggable HTTP transport for the API client."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Callable, Iterator, Mapping, Optional, Tuple, Union

from requests import Response
from typing_extensions import Self

from office365.runtime.http.request_options import RequestOptions

#: Default slice size (bytes) used by the streaming helpers.
DEFAULT_STREAM_CHUNK_SIZE = 8192

#: Default connect timeout (seconds) used by the bundled transports. It bounds
#: connection establishment without capping long transfers, because the read
#: phase stays unbounded (``None``).
DEFAULT_CONNECT_TIMEOUT = 10.0

HeadersCallback = Callable[[Mapping[str, str]], None]


class NoTimeoutType:
    """Sentinel type for :data:`NO_TIMEOUT`."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NO_TIMEOUT"


#: Pass as ``timeout`` to a bundled transport to disable its default timeout.
NO_TIMEOUT = NoTimeoutType()

#: A transport-level timeout: a single number or a ``(connect, read)`` tuple.
TimeoutValue = Union[float, Tuple[float, Optional[float]]]


class BaseTransport(ABC):
    """Abstract HTTP transport layer.

    Implementations handle the actual HTTP request/response cycle.
    The default implementation uses ``requests.Session``.

    Every transport is usable in both synchronous (:meth:`execute`) and
    asynchronous (:meth:`execute_async`) code. The async path defaults to
    offloading :meth:`execute` to a worker thread, so a transport backed by a
    blocking client (e.g. ``requests``) needs no async-specific code.
    """

    @abstractmethod
    def execute(self, request: RequestOptions) -> Response:
        """Send an HTTP request and return the response."""

    async def execute_async(self, request: RequestOptions) -> Response:
        """Send an HTTP request and return the response, without blocking the loop.

        The default implementation runs the blocking :meth:`execute` in a worker
        thread, so every transport becomes awaitable as-is and the underlying
        session (auth, proxies, connection reuse, rate limiting) is shared with
        the synchronous path.

        Transports with a native async engine override this method.

        Args:
            request: The request to send.

        Returns:
            The HTTP response.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.execute, request)

    def stream(
        self,
        request: RequestOptions,
        chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
        on_headers: Optional[HeadersCallback] = None,
    ) -> Iterator[bytes]:
        """Send a request and yield the response body incrementally.

        The default implementation sets ``request.stream``, delegates the send to
        :meth:`execute` — so auth, pacing, proxies and connection reuse are
        unchanged — and iterates the body in ``chunk_size`` slices. The response
        is closed when iteration finishes, the caller stops early, or an error
        occurs.

        Args:
            request: The request to send.
            chunk_size: Number of bytes per chunk.
            on_headers: Optional callback invoked once with the response headers
                before the first chunk (e.g. to read ``Content-Length``).

        Yields:
            The response body in ``chunk_size`` slices.

        Raises:
            requests.HTTPError: When the server returns an error status.
        """
        request.stream = True
        response = self.execute(request)
        try:
            response.raise_for_status()
            if on_headers is not None:
                on_headers(response.headers)
            yield from response.iter_content(chunk_size=chunk_size)
        finally:
            response.close()

    async def stream_async(
        self,
        request: RequestOptions,
        chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
        on_headers: Optional[HeadersCallback] = None,
    ) -> AsyncIterator[bytes]:
        """Async twin of :meth:`stream` that never blocks the event loop.

        Transports with a native async streaming engine override this. The
        default implementation drives the blocking :meth:`stream` in a worker
        thread one chunk per wait, so the loop stays free while a
        ``requests``-backed response body is read.

        Args:
            request: The request to send.
            chunk_size: Number of bytes per chunk.
            on_headers: Optional callback invoked once with the response headers
                before the first chunk.

        Yields:
            The response body in ``chunk_size`` slices.
        """
        loop = asyncio.get_running_loop()
        iterator = self.stream(request, chunk_size=chunk_size, on_headers=on_headers)

        def _next_chunk() -> Optional[bytes]:
            try:
                return next(iterator)
            except StopIteration:
                return None

        try:
            while True:
                chunk = await loop.run_in_executor(None, _next_chunk)
                if chunk is None:
                    break
                yield chunk
        finally:
            close = getattr(iterator, "close", None)
            if close is not None:
                await loop.run_in_executor(None, close)

    @property
    def proxies(self) -> dict[str, str] | None:
        """Transport-level proxy configuration."""
        return None

    @property
    def verify(self) -> bool | str:
        """Transport-level SSL verification."""
        return True

    @property
    def timeout(self) -> Optional[TimeoutValue]:
        """Transport-level request timeout in seconds."""
        return None

    @property
    def auth(self) -> Any | None:
        """Transport-level authentication handler, e.g. ``session.auth``."""
        return None

    def reset_connections(self) -> None:  # noqa: B027
        """Discard pooled connections so the next request opens a fresh one.

        Called before retrying a ``502``/``503``/``504`` or connection failure so
        a poisoned keep-alive socket is not reused (Microsoft Graph best
        practices). The default is a no-op; transports that pool connections
        override it.
        """

    def close(self) -> None:  # noqa: B027
        """Release transport resources (connections, etc.)."""

    async def aclose(self) -> None:
        """Asynchronously release transport resources.

        Default: run the synchronous :meth:`close` in a worker thread. Native
        async transports override this to await their own shutdown.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.close)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
