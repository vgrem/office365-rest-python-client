from __future__ import annotations

from typing import TYPE_CHECKING, Any

from office365.runtime.queries.client_query import ClientQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class PendingQuery(ClientQuery[Any]):
    """Placeholder query for ensure_property when property is already cached.
    Uses binding_type to hit the entity's own API URL, refreshing data from server.
    """

    def __init__(self, context, client_object: ClientObject):
        super().__init__(context, binding_type=client_object, return_type=client_object)
