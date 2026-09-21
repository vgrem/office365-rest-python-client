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
from office365.runtime.limits import Limit, LimitDecl, collect_class_limits, collect_limit_meta
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.read_entity import ReadEntityQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject
    from office365.runtime.http.throttling import RateLimiter
    from office365.runtime.queries.batch import BatchQuery


class ClientRuntimeContext(ABC):
    """Abstract base class for client runtime context.

    Provides core functionality for executing queries and managing request lifecycle.
    """

    _limit_meta: dict[str, Tuple[LimitDecl, ...]] = {}
    _class_limit_decls: Tuple[LimitDecl, ...] = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls._limit_meta = collect_limit_meta(cls)
        cls._class_limit_decls = collect_class_limits(cls)

    def __init__(self) -> None:
        self._queries: deque[ClientQuery] = deque()
        self._current_query = None
        self._pending_request: ClientRequest | None = None

    @classmethod
    def declared_limits(cls) -> Tuple[Limit, ...]:
        """The limits declared on this class and its methods/properties (``@limit``)."""
        class_limits = tuple(decl.limit for decl in cls._class_limit_decls)
        member_limits = tuple(decl.limit for decls in cls._limit_meta.values() for decl in decls)
        return (*class_limits, *member_limits)

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
        max_delay: Optional[int] = None,
        jitter: bool = True,
        success_callback: Optional[Callable[[ClientObject | None], None]] = None,
        failure_callback: Optional[Callable[[int, Exception], Optional[int]]] = None,
        exceptions: Tuple[Type[Exception], ...] = (ClientRequestException,),
    ) -> None:
        """Executes pending queries with retry logic.

        Only transient failures (HTTP 408/429/500/502/503/504 or non-HTTP errors)
        are retried. Permanent failures (e.g. HTTP 400/401/403/404) are re-raised
        immediately, and the last exception is re-raised once retries are exhausted.

        Delays between attempts use exponential backoff with jitter; a delay
        returned by ``failure_callback`` (e.g. the server's ``Retry-After`` via
        ``retry_after_delay``) overrides the backoff.

        Args:
            max_retry: Maximum number of retry attempts
            timeout_secs: Base delay for exponential backoff (seconds)
            max_delay: Optional cap on the exponential delay (seconds)
            jitter: Whether to randomize the delay (default True)
            success_callback: Called on successful execution
            failure_callback: Called after each failed attempt; may return a
                retry delay in seconds to override the backoff
            exceptions: Exception types that trigger retries
        """
        from office365.runtime.retry import retry

        def _on_failure(_attempt: int, ex: Exception) -> Optional[int]:
            # Re-queue the failed query for a retry, except on the last attempt —
            # otherwise the context is left with a stale, un-executed query.
            if _attempt < max_retry and self.current_query is not None:
                self.add_query(self.current_query)
            return failure_callback(_attempt, ex) if callable(failure_callback) else None

        def _on_success(_) -> None:
            if callable(success_callback) and self.current_query is not None:
                success_callback(self.current_query.return_type)

        try:
            retry(
                self.execute_query,
                max_retry=max_retry,
                timeout_secs=timeout_secs,
                max_delay=max_delay,
                jitter=jitter,
                exceptions=exceptions,
                on_failure=_on_failure,
                on_success=_on_success,
            )
        except BaseException:
            self._clear_retry_state()
            raise

    def _clear_retry_state(self) -> None:
        """Undo any failed-query re-queue and reset the cursor after an error.

        Called when ``execute_query_retry`` exits by exception so the context is
        never left dirty (a re-queued query would otherwise be re-run on reuse).
        """
        current = self._current_query
        if current is not None and self._queries and self._queries[-1] is current:
            self._queries.pop()
        self._current_query = None

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
        """Attach an error handler for the pending query — the error is swallowed.

        This is a control hook (see :meth:`ClientRequest.on_error`): once a
        handler is attached, a failing query is considered handled and does not
        re-raise. Use ``after_execute`` / ``throttle_guard`` for observation.
        """
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

    @property
    def rate_limiter(self) -> "RateLimiter | None":
        """The shared rate limiter pacing this context's requests, if any.

        Returns ``None`` until :meth:`with_rate_limit` (or a shared limiter via
        ``ClientRequest.with_rate_limiter``) is configured.
        """
        return self.pending_request().rate_limiter

    def with_rate_limit(self, health_threshold: int = 80, min_interval: float = 0.0) -> Self:
        """Enable fleet-wide pacing for this context (opt-in).

        Wraps the context transport with a shared rate limiter, so every request
        — including the parallel batches dispatched by ``execute_batch`` — is
        gated by ``Retry-After`` / ``X-SharePointHealthScore`` as a group. Call
        this after any transport configuration (``with_transport``).

        Args:
            health_threshold: Health score at/above which the group paces.
            min_interval: Minimum pause applied on a high health score (seconds).

        Returns:
            Self: Supports method chaining
        """
        self.pending_request().with_rate_limit(health_threshold=health_threshold, min_interval=min_interval)
        return self

    def execute_query(self) -> Self:
        """Executes all pending queries.

        Returns:
            Self for method chaining
        """
        while self.has_pending_request:
            qry = self._get_next_query()
            qry.execute_query(self.pending_request())
        return self

    def execute_query_parallel(
        self,
        concurrency: int = 4,
        progress: Optional[Callable[[Any], None]] = None,
        max_retry: int = 5,
        timeout_secs: int = 5,
        max_delay: Optional[int] = None,
        jitter: bool = True,
    ) -> Self:
        """Executes pending queries concurrently, overlapping their HTTP I/O.

        Intended for **independent** queries (e.g. bulk downloads: queue each
        ``item.download(f)`` then call this once). Query lifecycle stays on the
        calling thread — ``before_execute``/``after_execute``/``on_error`` hooks
        fire as usual — only the network round-trips run on the pool. Transient
        failures (408/429/5xx) are retried per query, honoring ``Retry-After``.

        Falls back to sequential :meth:`execute_query` when ``concurrency <= 1``
        or when the context uses a non-standard request (e.g. an upload session).

        Args:
            concurrency: Maximum number of concurrent requests.
            progress: Optional hook fired per completed query with a ``Progress``
              snapshot (``done``/``total``).
            max_retry: Maximum retry attempts per query.
            timeout_secs: Base delay for exponential backoff (seconds).
            max_delay: Optional cap on the exponential delay (seconds).
            jitter: Whether to randomize the backoff delay.

        Returns:
            Self for method chaining
        """
        if concurrency <= 1 or not self.has_pending_request:
            return self.execute_query()

        request = self.pending_request()
        if type(request).execute_query is not ClientRequest.execute_query:
            return self.execute_query()

        from office365.runtime.parallel import run_parallel

        def _send(_ctx, task: Tuple[ClientQuery, RequestOptions]):
            return self._send_with_retry(request, task[1], max_retry, timeout_secs, max_delay, jitter)

        while self.has_pending_request:
            prepared: List[Tuple[ClientQuery, RequestOptions]] = []
            while self.has_pending_request:
                qry = self._get_next_query()
                if type(qry).execute_query is not ClientQuery.execute_query:
                    qry.execute_query(request)  # deferred/no-op queries stay sequential
                    continue
                options = request.build_request(qry)
                request.beforeExecute(options)
                prepared.append((qry, options))
            if not prepared:
                break

            responses = run_parallel(
                _send,
                prepared,
                concurrency=concurrency,
                progress=progress,
                on_error=lambda _task, error: error,
            )

            for index, ((qry, _options), response) in enumerate(zip(prepared, responses)):
                if isinstance(response, BaseException):
                    for pending, _ in prepared[index:]:  # keep failed + unhandled queries
                        self._queries.append(pending)
                    self._current_query = None
                    raise response
                self._current_query = qry
                request._raise_for_status(response)
                request.process_response(response, qry)
                request.afterExecute(response)
        self._current_query = None
        return self

    @staticmethod
    def _send_with_retry(
        request: ClientRequest,
        options: RequestOptions,
        max_retry: int,
        timeout_secs: int,
        max_delay: Optional[int],
        jitter: bool,
    ):
        """Send one prepared request, retrying transient failures per ``Retry-After``."""
        from office365.runtime.retry import TRANSIENT_STATUS_CODES, response_retry_after, retry

        def _attempt():
            response = request.transport.execute(options)
            if response.status_code in TRANSIENT_STATUS_CODES:
                raise ClientRequestException.from_response(response)
            return response

        return retry(
            _attempt,
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            max_delay=max_delay,
            jitter=jitter,
            on_failure=lambda _attempt_num, ex: response_retry_after(getattr(ex, "response", None)),
        )

    def add_query(self, query: ClientQuery) -> Self:
        """Adds a query to the pending queue.

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

    def _split_batches(
        self,
        items_per_batch: int,
        max_batch_bytes: Optional[int] = None,
    ) -> list["BatchQuery"]:
        """Drain the pending queue into independent batch units.

        Unlike ``_get_next_query``, this does not mutate ``_current_query``,
        making it safe to pre-split the queue before concurrent execution.
        Batches are capped by item count and (when ``max_batch_bytes`` is given)
        by estimated payload size — a single oversized query still goes alone.

        Args:
            items_per_batch: Maximum queries per batch
            max_batch_bytes: Maximum estimated batch payload size in bytes

        Returns:
            List of BatchQuery objects preserving submission order
        """
        from office365.runtime.odata.batch_util import partition_by_limits
        from office365.runtime.queries.batch import BatchQuery

        queries = []
        while self.has_pending_request:
            queries.append(self._queries.popleft())

        batches = []
        for chunk in partition_by_limits(queries, items_per_batch, max_batch_bytes):
            batches.append(BatchQuery(self, chunk))
        return batches

    def _execute_batches_in_parallel(
        self,
        batches: list["BatchQuery"],
        concurrency: int,
        success_callback: Optional[Callable[[List[Any]], None]] = None,
    ) -> None:
        """Execute batch units concurrently on a thread pool.

        Reuses the generic :func:`~office365.runtime.parallel.run_parallel`
        primitive; ``success_callback`` is invoked **live, as each batch
        completes** (on the calling thread), so callers can report progress.
        After the pool drains, the first failure is re-raised.

        Args:
            batches: Batch units to execute
            concurrency: Maximum number of concurrent batch requests
            success_callback: Called with each successfully completed batch's
                return types, in completion order
        """
        from office365.runtime.parallel import run_parallel

        errors: list[BaseException] = []

        def _on_progress(snapshot: Any) -> None:
            if not callable(success_callback):
                return
            for return_types in snapshot.items or []:
                if return_types is not None:
                    success_callback(return_types)

        def _on_error(_task: Any, error: BaseException) -> None:
            errors.append(error)

        run_parallel(
            lambda _ctx, batch_qry: self._execute_batch(batch_qry),
            batches,
            concurrency=concurrency,
            progress=_on_progress,
            on_error=_on_error,
        )
        if errors:
            raise errors[0]

    def _execute_batch(self, batch_qry: "BatchQuery") -> List[Any]:
        """Execute a single batch unit (implemented by concrete contexts)."""
        raise NotImplementedError
