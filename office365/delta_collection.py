from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional, Type

from typing_extensions import Self

from office365.delta_path import DeltaPath
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_object import T
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class ChangeType(Enum):
    """"""

    created = "0"
    updated = "1"
    deleted = "2"


class DeltaCollection(EntityCollection[T]):
    """
    A specialized collection that tracks changes (deltas) to entities over time.

    This collection supports:
    - Change tracking via delta tokens
    - Filtering changes by type (created, updated, deleted)
    - Seamless delta query pagination

    Typical usage:
        >>> client = GraphClient()
        >>> inbox = client.me.mail_folders["Inbox"]
        >>> changes = inbox.messages.delta.change_type(ChangeType.created).get().execute_query()
    """

    def __init__(
        self,
        context: GraphClient,
        item_type: Type[T],
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[Entity] = None,
    ):
        super(DeltaCollection, self).__init__(context, item_type, resource_path, parent)

    def change_type(self, type_name: ChangeType) -> Self:
        """
        Filter the delta response to only include changes of the specified type.

        Supported change types:
        - "created": Only newly created items
        - "updated": Only modified items
        - "deleted": Only deleted items

        Args:
            type_name: The change type to filter by

        Returns:
            self: Supports method chaining
        """
        self.query_options.custom["changeType"] = type_name.name
        return self

    @property
    def delta(self) -> DeltaCollection[T]:
        """
        Gets a new delta collection for tracking subsequent changes.

        This property implements the delta link pattern for tracking changes over time.
        The returned collection will only contain items that changed since the last request.

        Returns:
            DeltaCollection: A new collection configured for delta tracking
        """
        return self.properties.get(
            "delta",
            DeltaCollection(
                self.context, self._item_type, DeltaPath(self.resource_path)
            ),
        )
