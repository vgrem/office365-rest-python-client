from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional

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
        self._service_root_url: str | None = None
        self.beforeExecute: EventHandler[[RequestOptions]] = EventHandler()
        self.afterExecute: EventHandler[[Response]] = EventHandler()

    @property
    def transport(self) -> BaseTransport:
        """The HTTP transport used for API requests."""
        return self._transport

    @transport.setter
    def transport(self, value: BaseTransport) -> None:
        self._transport = value

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

    def set_service_root(self, url: str) -> None:
        """Update the service root URL. Subclasses may additionally sync auth state."""
        self._service_root_url = url

    def execute_query(self, query: ClientQuery) -> None:
        """Submits a pending request to the server"""
        try:
            request = self.build_request(query)
            self.beforeExecute(request)
            response = self.execute_request_direct(request)
            self.process_response(response, query)
            self.afterExecute(response)
        except HTTPError as e:
            raise ClientRequestException(*e.args, response=e.response) from e

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
        action: Callable[[Response], None],
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

    def execute_request_direct(self, request: RequestOptions) -> Response:
        """Execute the client request"""
        self.beforeExecute(request)
        response = self._transport.execute(request)
        response.raise_for_status()
        return response
