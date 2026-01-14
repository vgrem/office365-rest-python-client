from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional

import requests
from requests import HTTPError, Response
from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.types.event_handler import EventHandler


class ClientRequest(ABC):
    def __init__(self):
        """
        Abstract request client
        """
        self.beforeExecute = EventHandler()
        self.afterExecute = EventHandler()

    @abstractmethod
    def build_request(self, query: ClientQuery) -> RequestOptions:
        """Transform query into request options

        Args:
            query: The client query to execute

        Returns:
            Configured RequestOptions object"""

    @abstractmethod
    def process_response(self, response: requests.Response, query: ClientQuery) -> None:
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
        if request.method == HttpMethod.Post:
            if request.is_bytes or request.is_file:
                response = requests.post(
                    url=request.url,
                    headers=request.headers,
                    data=request.data,
                    auth=request.auth,
                    verify=request.verify,
                    proxies=request.proxies,
                    timeout=request.timeout,
                )
            else:
                response = requests.post(
                    url=request.url,
                    headers=request.headers,
                    json=request.data,
                    auth=request.auth,
                    verify=request.verify,
                    proxies=request.proxies,
                    timeout=request.timeout,
                )
        elif request.method == HttpMethod.Patch:
            response = requests.patch(
                url=request.url,
                headers=request.headers,
                json=request.data,
                auth=request.auth,
                verify=request.verify,
                proxies=request.proxies,
                timeout=request.timeout,
            )
        elif request.method == HttpMethod.Delete:
            response = requests.delete(
                url=request.url,
                headers=request.headers,
                auth=request.auth,
                verify=request.verify,
                proxies=request.proxies,
                timeout=request.timeout,
            )
        elif request.method == HttpMethod.Put:
            response = requests.put(
                url=request.url,
                data=request.data,
                headers=request.headers,
                auth=request.auth,
                verify=request.verify,
                proxies=request.proxies,
                timeout=request.timeout,
            )
        else:
            response = requests.get(
                url=request.url,
                headers=request.headers,
                auth=request.auth,
                verify=request.verify,
                stream=request.stream,
                proxies=request.proxies,
                timeout=request.timeout,
            )
        response.raise_for_status()
        return response
