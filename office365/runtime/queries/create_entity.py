from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from office365.runtime.client_value import ClientValue
from office365.runtime.queries.client_query import ClientQuery, ReturnT

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class CreateEntityQuery(ClientQuery[ReturnT]):
    def __init__(
        self,
        parent_entity: ClientObject,
        parameters: ClientObject | ClientValue | Dict | str | bytes | None,
        return_type: ReturnT | None = None,
    ):
        """Create entity query.

        ``parameters`` is normally the entity to create, which the query serializes. A
        raw ``str``/``bytes`` body is legal too, for an endpoint whose create contract is
        a document rather than a JSON object (a MIME import posts base64 text).
        """
        super().__init__(parent_entity.context, parent_entity, parameters, None, return_type)
