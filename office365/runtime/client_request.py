from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

import requests
from requests import HTTPError, Response
from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.transport.base import BaseTransport
from office365.runtime.transport.requests_transport import RequestsTransport
from office365.runtime.types.event_handler import EventHandler


class ClientRequest(ABC):
    def __init__(self, transport: BaseTransport | None = None):
        self._transport = transport or RequestsTransport()
        self.beforeExecute: EventHandler[[RequestOptions]] = EventHandler()
        self.afterExecute: EventHandler[[Response]] = EventHandler()
        self.onError: EventHandler[[ClientRequestException]] = EventHandler()

    @property
    def transport(self) -> BaseTransport:
        """The HTTP transport used for API requests."""
        return self._transport

    @transport.setter
    def transport(self, value: BaseTransport) -> None:
        self._transport = value

    def with_transport(
        self,
        proxies: dict[str, str] | None = None,
        verify: bool | str | None = None,
        timeout: int | tuple[int, int] | None = None,
        session: requests.Session | None = None,
    ) -> Self:
        """Configure the HTTP transport (proxy, SSL, timeout, custom session).

        All parameters are optional.  Per-request values (``request.proxies``,
        ``request.verify``) take precedence over transport-level values.

        Args:
            proxies: Proxy URLs (e.g. ``{"https": "http://proxy:8080"}``)
            verify: SSL verification — ``True``, ``False``, or a CA bundle path
            timeout: Request timeout in seconds
            session: Custom ``requests.Session`` with pre-configured adapters

        Returns:
            Self: Supports method chaining
        """
        self._transport = RequestsTransport(
            session=session,
            proxies=proxies,
            verify=True if verify is None else verify,
            timeout=timeout,
        )
        return self

    @property
    @abstractmethod
    def service_root_url(self) -> str:
        """Gets the service root URL."""

    @abstractmethod
    def build_request(self, query: ClientQuery) -> RequestOptions:
        """Transform query into request options

        Args:
            query: The client query to execute

        Returns:
            Configured RequestOptions object"""

    @abstractmethod
    def process_response(self, response: Response, query: ClientQuery) -> None:
        """Handle and transform the response

        Args:
            response: Raw HTTP response
            query: Original query that generated this response"""

    def execute_query(self, query: ClientQuery) -> None:
        """Submits a pending request to the server"""
        try:
            request = self.build_request(query)
            response = self.execute_request_direct(request)
            self.process_response(response, query)
            self.afterExecute(response)
        except ClientRequestException as e:
            if self.onError:
                self.onError(e)
                return
            raise
        except HTTPError as e:
            raise ClientRequestException.from_response(e.response) from e

    def on_error(
        self,
        action: Callable[[ClientRequestException], None],
        once: bool = True,
        condition: Optional[Callable[[], bool]] = None,
    ) -> Self:
        def _process_error(e: ClientRequestException):
            matches = condition is None or condition()
            if matches:
                if once:
                    self.onError -= _process_error
                action(e)

        self.onError += _process_error
        return self

    def before_execute(
        self,
        action: Callable[[RequestOptions], None],
        once: bool = True,
        condition: Optional[Callable[[], bool]] = None,
    ) -> Self:
        """Attaches pre-query execution handler.

        Args:
            action: Callback to execute before query
            once: Whether to execute only once
            condition: Optional condition to check before executing action

        Returns:
            Self for method chaining
        """

        def _process_request(request: RequestOptions):
            if condition is None or condition():
                if once:
                    self.beforeExecute -= _process_request
                action(request)

        self.beforeExecute += _process_request
        return self

    def after_execute(
        self,
        action: Callable[[Response], Any],
        once: bool = True,
        condition: Optional[Callable[[], bool]] = None,
    ) -> Self:
        """Attaches post-execution handler for all requests.

        Args:
            action: Callback to execute after request
            once: Whether to execute only once
            condition: Optional condition to check before executing action

        Returns:
            Self for method chaining
        """

        def _process_response(response: Response) -> None:
            if condition is None or condition():
                if once:
                    self.afterExecute -= _process_response
                action(response)

        self.afterExecute += _process_response
        return self

    @staticmethod
    def _raise_for_status(response: Response) -> None:
        """Check HTTP status and dispatch to the right exception type via the factory."""
        try:
            response.raise_for_status()
        except HTTPError:
            raise ClientRequestException.from_response(response) from None

    def execute_request_direct(self, request: RequestOptions) -> Response:
        """Execute the client request"""
        self.beforeExecute(request)
        response = self._transport.execute(request)
        self._raise_for_status(response)
        return response

    def execute_request(self, path: str) -> Response:
        """Executes request directly against the specified path.

        Args:
            path: The URL path to request

        Returns:
            Raw response from server
        """
        full_url = "".join([self.service_root_url, "/", path])
        request = RequestOptions(url=full_url)
        return self.execute_request_direct(request)
