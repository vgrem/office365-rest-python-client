from __future__ import annotations

from typing import TYPE_CHECKING, cast

from office365.runtime.queries.client_query import ClientQuery, T

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext


class PendingQuery(ClientQuery[T]):
    """A query placeholder that will be resolved with an actual query"""

    def __init__(self, context: ClientRuntimeContext):
        super().__init__(context)

    def resolve(self, query: ClientQuery[T]):
        """Resolve this pending query with an actual query"""
        self.__dict__.update(query.__dict__)
        self.__class__ = cast(type, query.__class__)
        return self
