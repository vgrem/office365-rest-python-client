from __future__ import annotations

import uuid

from typing_extensions import Self

from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.queries.client_query import ClientQuery, T
from office365.runtime.queries.read_entity import ReadEntityQuery


def create_boundary(prefix: str, compact: bool = False) -> str:
    """Creates a string that can be used as a multipart request boundary.

    Args:
        prefix: String to use as the start of the boundary string
        compact: If True, generates a shorter boundary string
    """
    if compact:
        return prefix + str(uuid.uuid4())[:8]
    else:
        return prefix + str(uuid.uuid4())


class BatchQuery(ClientQuery[T]):
    """Client query collection for batch requests."""

    def __init__(self, context: ClientRuntimeContext, queries: list[ClientQuery] | None = None) -> None:
        """
        Initialize a batch query collection.

        Args:
            context: Client runtime context
            queries: List of queries to include in the batch (optional)
        """
        super().__init__(context)
        self._current_boundary = create_boundary("batch_")
        if queries is None:
            queries = []
        self._queries = queries

    def add(self, query: ClientQuery) -> Self:
        """Add a query to the batch.

        Args:
            query: The query to add to the batch
        """
        self._queries.append(query)
        return self

    @property
    def ordered_queries(self) -> list[ClientQuery]:
        """Returns all queries in execution order (change sets first, then GET queries)."""
        return self.change_sets + self.get_queries

    @property
    def current_boundary(self) -> str:
        """Gets the current multipart boundary string."""
        return self._current_boundary

    @property
    def change_sets(self) -> list[ClientQuery]:
        """Gets all queries that modify data (non-GET operations)."""
        return [qry for qry in self._queries if not isinstance(qry, ReadEntityQuery)]

    @property
    def queries(self) -> list[ClientQuery]:
        """Gets all queries in the batch."""
        return self._queries

    @property
    def get_queries(self) -> list[ClientQuery]:
        """Gets all read-only (GET) queries in the batch."""
        return [qry for qry in self._queries if isinstance(qry, ReadEntityQuery)]

    @property
    def has_change_sets(self) -> bool:
        """Determines whether the batch contains any data modification operations."""
        return len(self.change_sets) > 0

    @property
    def url(self) -> str:
        """Gets the batch request URL."""
        return f"{self.context.service_root_url}/$batch"

    @property
    def return_type(self) -> list[T]:  # type:ignore
        """Gets the return types of all queries in the batch."""
        return [q.return_type for q in self._queries if q.return_type]
