from abc import ABC, abstractmethod
from time import sleep
from typing import TYPE_CHECKING, AnyStr, Callable, List, Optional, Tuple, Type, Union

from requests import RequestException, Response
from typing_extensions import Self

from office365.runtime.client_request import ClientRequest
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.read_entity import ReadEntityQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject, T


class ClientRuntimeContext(ABC):
    """Abstract base class for client runtime context.

    Provides core functionality for executing queries and managing request lifecycle.
    """

    def __init__(self) -> None:
        self._queries = []
        self._current_query = None

    @property
    def current_query(self) -> ClientQuery:
        return self._current_query

    @property
    def has_pending_request(self) -> bool:
        """Whether there are pending queries to execute."""
        return len(self._queries) > 0

    def build_request(self, query: ClientQuery) -> RequestOptions:
        """Builds a request from the given query.

        Args:
            query: The query to build request for

        Returns:
            Configured request options
        """
        self._current_query = query
        request = self.pending_request().build_request(query)
        self.pending_request().beforeExecute.notify(request)
        return request

    def execute_query_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        success_callback: Optional[Callable[["ClientObject"], None]] = None,
        failure_callback: Optional[Callable[[int, RequestException], None]] = None,
        exceptions: Tuple[Type[Exception], ...] = (ClientRequestException,),
    ):
        """Executes pending queries with retry logic.

        Args:
            max_retry: Maximum number of retry attempts
            timeout_secs: Delay between retries in seconds
            success_callback: Called on successful execution
            failure_callback: Called after each failed attempt
            exceptions: Exception types that trigger retries
        """

        for retry in range(1, max_retry + 1):
            try:
                self.execute_query()
                if callable(success_callback):
                    success_callback(self.current_query.return_type)
                break
            except exceptions as e:
                self.add_query(self.current_query)
                if callable(failure_callback):
                    failure_callback(retry, e)
                sleep(timeout_secs)

    @abstractmethod
    def pending_request(self) -> ClientRequest:
        """Gets the pending client request."""
        pass

    @property
    @abstractmethod
    def service_root_url(self) -> str:
        """Gets the service root URL."""
        pass

    def load(
        self, client_object: "T", properties_to_retrieve: List[str] = None
    ) -> Self:
        """Prepares retrieval query for the specified client object.

        Args:
            client_object: The client object to load
            properties_to_retrieve: Specific properties to retrieve

        Returns:
            Self for method chaining
        """
        qry = ReadEntityQuery(client_object, properties_to_retrieve)
        self.add_query(qry)
        return self

    def before_query_execute(
        self, action: Callable[[RequestOptions], None], once: bool = True
    ) -> Self:
        """
        Attach an event handler which is triggered before query is submitted to server
        """
        if len(self._queries) == 0:
            return self
        query = self._queries[-1]

        def _prepare_request(request: RequestOptions) -> None:
            if self.current_query.id == query.id:
                if once:
                    self.pending_request().beforeExecute -= _prepare_request
                action(request)

        self.pending_request().beforeExecute += _prepare_request
        return self

    def before_execute(
        self, action: Callable[[RequestOptions], None], once: bool = True
    ) -> Self:
        """Attaches pre-query execution handler.

        Args:
            action: Callback to execute before query
            once: Whether to execute only once

        Returns:
            Self for method chaining
        """

        def _process_request(request: RequestOptions):
            if once:
                self.pending_request().beforeExecute -= _process_request
            action(request)

        self.pending_request().beforeExecute += _process_request
        return self

    def after_query_execute(
        self,
        action: Callable[[Union["T", Response]], None],
        execute_first: bool = False,
        include_response: bool = False,
    ) -> Self:
        """Attaches post-query execution handler.

        Args:
            action: Callback to execute after query
            execute_first: Whether to prioritize this query
            include_response: Whether to pass raw response

        Returns:
            Self for method chaining
        """
        if len(self._queries) == 0:
            return self
        query = self._queries[-1]

        def _process_response(resp: Response) -> None:
            resp.raise_for_status()
            if self.current_query.id == query.id:
                self.pending_request().afterExecute -= _process_response
                action(resp if include_response else query.return_type)

        self.pending_request().afterExecute += _process_response

        if execute_first and len(self._queries) > 1:
            self._queries.insert(0, self._queries.pop())

        return self

    def after_execute(
        self, action: Callable[[Response], None], once: bool = True
    ) -> Self:
        """Attaches post-execution handler for all requests.

        Args:
            action: Callback to execute after request
            once: Whether to execute only once

        Returns:
            Self for method chaining
        """

        def _process_response(response: Response) -> None:
            if once:
                self.pending_request().afterExecute -= _process_response
            action(response)

        self.pending_request().afterExecute += _process_response
        return self

    def execute_request_direct(self, path: str) -> Response:
        """Executes request directly against the specified path.

        Args:
            path: The URL path to request

        Returns:
            Raw response from server
        """
        full_url = "".join([self.service_root_url, "/", path])
        request = RequestOptions(url=full_url)
        return self.pending_request().execute_request_direct(request)

    def execute_query(self) -> Self:
        """Executes all pending queries.

        Returns:
            Self for method chaining
        """
        while self.has_pending_request:
            qry = self._get_next_query()
            self.pending_request().execute_query(qry)
        return self

    def add_query(self, query: ClientQuery) -> Self:
        """Adds query to the pending queue.

        Args:
            query: The query to add

        Returns:
            Self for method chaining
        """
        self._queries.append(query)
        return self

    def clear(self) -> Self:
        """Clears all pending queries.

        Returns:
            Self for method chaining
        """
        self._current_query = None
        self._queries = []
        return self

    def get_metadata(self) -> ClientResult[AnyStr]:
        """Retrieves service metadata.

        Returns:
            ClientResult containing metadata XML
        """
        return_type = ClientResult(self)

        def _construct_request(request: RequestOptions) -> None:
            request.url += "/$metadata"
            request.method = HttpMethod.Get

        def _process_response(response: Response) -> None:
            response.raise_for_status()
            return_type.set_property("__value", response.content)

        qry = ClientQuery(self)
        (
            self.add_query(qry)
            .before_execute(_construct_request)
            .after_execute(_process_response)
        )
        return return_type

    def _get_next_query(self, count: int = 1) -> ClientQuery:
        """Gets the next query(s) to execute.

        Args:
            count: Number of queries to batch together

        Returns:
            The next query to execute
        """
        if count == 1:
            qry = self._queries.pop(0)
        else:
            from office365.runtime.queries.batch import BatchQuery

            qry = BatchQuery(self)
            while self.has_pending_request and count > 0:
                qry.add(self._queries.pop(0))
                count = count - 1
        self._current_query = qry
        return qry
