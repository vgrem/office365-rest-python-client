"""A placeholder query that defers an operation until it resolves.

Implements a lightweight promise: the placeholder occupies a fixed slot in the
pending queue; when the prerequisite resolves, :meth:`defer` swaps the slot for
the real operation (e.g. a field create) or :meth:`resolve` drops it. The query
loop therefore only ever executes real operations, and anything queued after the
placeholder always runs after the operation completes — no queue reordering.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from typing_extensions import Self

from office365.runtime.queries.client_query import ClientQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class DeferredOperationQuery(ClientQuery[Any]):
    """A queue placeholder that resolves to a deferred operation."""

    def __init__(self, context, return_type: Optional["ClientObject"] = None):
        super().__init__(context, return_type=return_type)
        self._deferred: Optional[ClientQuery] = None

    def defer(self, query: ClientQuery) -> Self:
        """Swap this placeholder's queue slot for the actual operation.

        The operation runs next (in this slot), before anything queued after
        the placeholder.
        """
        self._deferred = query
        queue = self.context._queries  # type: ignore[attr-defined]
        try:
            queue[queue.index(self)] = query
        except ValueError:
            pass
        return self

    def resolve(self) -> None:
        """Drop this placeholder from the queue (no operation is needed)."""
        queue = self.context._queries  # type: ignore[attr-defined]
        try:
            queue.remove(self)
        except ValueError:
            pass

    @property
    def deferred_query(self) -> Optional[ClientQuery]:
        """The attached operation, or ``None`` when not deferred."""
        return self._deferred
