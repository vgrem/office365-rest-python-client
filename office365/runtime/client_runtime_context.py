from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Type

from requests import Response
from typing_extensions import Self

from office365.runtime.client_request import ClientRequest
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.read_entity import ReadEntityQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.queries.batch import BatchQuery


class ClientRuntimeContext(ABC):
    """Abstract base class for client runtime context.

    Provides core functionality for executing queries and managing request lifecycle.
    """

    def __init__(self) -> None:
        self._queries: deque[ClientQuery] = deque()
        self._current_query = None
        self._pending_request: ClientRequest | None = None

    @property
    def service_root_url(self) -> str:
        """Get the API service root URL"""
        return self.pending_request().service_root_url

    @property
    def current_query(self) -> ClientQuery | None:
        return self._current_query

    @property
    def has_pending_request(self) -> bool:
        """Whether there are pending queries to execute."""
        return len(self._queries) > 0

    def execute_query_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        success_callback: Optional[Callable[[ClientObject | None], None]] = None,
        failure_callback: Optional[Callable[[int, Exception], Optional[int]]] = None,
        exceptions: Tuple[Type[Exception], ...] = (ClientRequestException,),
    ) -> None:
        """Executes pending queries with retry logic.

        Only transient failures (HTTP 408/429/500/502/503/504 or non-HTTP errors)
        are retried. Permanent failures (e.g. HTTP 400/401/403/404) are re-raised
        immediately, and the last exception is re-raised once retries are exhausted.

        Args:
            max_retry: Maximum number of retry attempts
            timeout_secs: Delay between retries in seconds
            success_callback: Called on successful execution
            failure_callback: Called after each failed attempt; may return a
                retry delay in seconds to override ``timeout_secs``
            exceptions: Exception types that trigger retries
        """
        from office365.runtime.retry import retry

        def _on_failure(_attempt: int, ex: Exception) -> Optional[int]:
            if self.current_query is not None:
                self.add_query(self.current_query)
            return failure_callback(_attempt, ex) if callable(failure_callback) else None

        def _on_success(_) -> None:
            if callable(success_callback) and self.current_query is not None:
                success_callback(self.current_query.return_type)

        retry(
            self.execute_query,
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            exceptions=exceptions,
            on_failure=_on_failure,
            on_success=_on_success,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        self.pending_request().transport.close()

    @abstractmethod
    def pending_request(self) -> ClientRequest:
        """Gets the pending client request."""

    def load(self, client_object: ClientObject, properties_to_retrieve: List[str] | None = None) -> Self:
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

    def before_execute(self, action: Callable[[RequestOptions], None], once: bool = True) -> Self:
        """
        Attach an event handler which is triggered before query is submitted to server
        """
        if len(self._queries) == 0:
            return self
        query = self._queries[-1]

        self.pending_request().before_execute(
            action, once=once, condition=lambda: self.current_query is not None and self.current_query.id == query.id
        )
        return self

    def after_execute(
        self,
        action: Callable[[Any], Any],
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
            if callable(action):
                action(resp if include_response else query.return_type)

        self.pending_request().after_execute(
            _process_response,
            once=True,
            condition=lambda: self.current_query is not None and self.current_query.id == query.id,
        )

        if execute_first and len(self._queries) > 1:
            self._queries.appendleft(self._queries.pop())

        return self

    def on_error(self, action: Callable[[ClientRequestException], None], once: bool = True) -> Self:
        if len(self._queries) == 0:
            return self
        query = self._queries[-1]

        self.pending_request().on_error(
            action,
            once=once,
            condition=lambda: self.current_query is not None and self.current_query.id == query.id,
        )
        return self

    def execute_request_direct(self, path: str) -> Response:
        """Executes request directly against the specified path.

        Args:
            path: The URL path to request

        Returns:
            Raw response from server
        """
        return self.pending_request().execute_request(path)

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
        """Clears pending state and resets the pending request.

        A new request is created lazily on the next call to ``pending_request()``.
        """
        self._current_query = None
        self._queries = deque()
        self._pending_request = None
        return self

    def get_metadata(self) -> ClientResult[bytes]:
        """Retrieves service metadata.

        Returns:
            ClientResult containing metadata XML
        """
        return_type = ClientResult(self, bytes())

        def _construct_request(request: RequestOptions) -> None:
            request.url += "/$metadata"
            request.method = HttpMethod.Get

        def _process_response(response: Response) -> None:
            return_type.set_property("__value", response.content)

        qry = ClientQuery(self)
        (self.add_query(qry).before_execute(_construct_request).after_execute(_process_response, include_response=True))
        return return_type

    def _get_next_query(self, count: int = 1) -> ClientQuery:
        """Gets the next query(s) to execute.

        Args:
            count: Number of queries to batch together

        Returns:
            The next query to execute
        """
        if count == 1:
            qry = self._queries.popleft()
        else:
            from office365.runtime.queries.batch import BatchQuery

            qry = BatchQuery(self)
            while self.has_pending_request and count > 0:
                qry.add(self._queries.popleft())
                count = count - 1
        self._current_query = qry
        return qry

    def _split_batches(self, items_per_batch: int) -> list["BatchQuery"]:
        """Drain the pending queue into independent batch units.

        Unlike ``_get_next_query``, this does not mutate ``_current_query``,
        making it safe to pre-split the queue before concurrent execution.

        Args:
            items_per_batch: Maximum queries per batch

        Returns:
            List of BatchQuery objects preserving submission order
        """
        from office365.runtime.queries.batch import BatchQuery

        batches = []
        while self.has_pending_request:
            qry = BatchQuery(self)
            count = 0
            while self.has_pending_request and count < items_per_batch:
                qry.add(self._queries.popleft())
                count = count + 1
            batches.append(qry)
        return batches

    def _execute_batches_in_parallel(
        self,
        batches: list["BatchQuery"],
        concurrency: int,
        success_callback: Optional[Callable[[List[Any]], None]] = None,
    ) -> None:
        """Execute batch units concurrently on a thread pool.

        Each batch runs ``self._execute_batch`` on a worker thread;
        ``success_callback`` is invoked on the caller thread in completion
        order. On the first failure, pending batches are cancelled and the
        exception is re-raised.

        Args:
            batches: Batch units to execute
            concurrency: Maximum number of concurrent batch requests
            success_callback: Called with each completed batch's return types
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(self._execute_batch, batch_qry) for batch_qry in batches]
            for future in as_completed(futures):
                try:
                    return_types = future.result()
                except Exception:
                    for f in futures:
                        f.cancel()
                    raise
                if callable(success_callback):
                    success_callback(return_types)

    def _execute_batch(self, batch_qry: "BatchQuery") -> List[Any]:
        """Execute a single batch unit (implemented by concrete contexts)."""
        raise NotImplementedError
