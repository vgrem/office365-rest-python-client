"""Pluggable HTTP transport for the API client."""

from __future__ import annotations

from abc import ABC, abstractmethod

from requests import Response
from typing_extensions import Self

from office365.runtime.http.request_options import RequestOptions


class BaseTransport(ABC):
    """Abstract HTTP transport layer.

    Implementations handle the actual HTTP request/response cycle.
    The default implementation uses ``requests.Session``.
    """

    @abstractmethod
    def execute(self, request: RequestOptions) -> Response:
        """Send an HTTP request and return the response."""

    def close(self) -> None:  # noqa: B027
        """Release transport resources (connections, etc.)."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
