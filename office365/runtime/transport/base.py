"""Pluggable HTTP transport for the API client."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Tuple

from requests import Response
from typing_extensions import Self

from office365.runtime.http.request_options import RequestOptions


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

    @property
    def proxies(self) -> dict[str, str] | None:
        """Transport-level proxy configuration."""
        return None

    @property
    def verify(self) -> bool | str:
        """Transport-level SSL verification."""
        return True

    @property
    def timeout(self) -> int | Tuple[int, int] | None:
        """Transport-level request timeout in seconds."""
        return None

    @property
    def auth(self) -> Any | None:
        """Transport-level authentication handler, e.g. ``session.auth``."""
        return None

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
