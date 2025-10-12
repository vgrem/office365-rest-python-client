from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union

from office365.runtime.client_value import ClientValue
from office365.runtime.queries.client_query import ClientQuery, T

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class CreateEntityQuery(ClientQuery[T]):
    def __init__(
        self, parent_entity: ClientObject, parameters: Union[ClientObject | ClientValue | Dict], return_type: T = None
    ):
        """Create entity query"""
        super().__init__(parent_entity.context, parent_entity, parameters, None, return_type)
