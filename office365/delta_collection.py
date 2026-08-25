from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Type

from typing_extensions import Self

from office365.delta_path import DeltaPath
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_object import ClientObjectT
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


_DELTA_TOKEN_PATTERN = re.compile(r"(?:[?&(])(?:token|\$deltatoken|\$skiptoken)\s*=\s*'?\s*([^&()'\s]+)")


def _extract_delta_token(delta_link: Optional[str]) -> Optional[str]:
    """Extract the resumable token value from an ``@odata.deltaLink``/nextLink URL."""
    if not delta_link:
        return None
    match = _DELTA_TOKEN_PATTERN.search(delta_link)
    return match.group(1) if match else None


class ChangeType(Enum):
    """"""

    created = "0"
    updated = "1"
    deleted = "2"


class DeltaCollection(EntityCollection[ClientObjectT]):
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
        item_type: Type[ClientObjectT],
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[Entity] = None,
    ):
        super().__init__(context, item_type, resource_path, parent)
        self._delta_request_url = None

    def token(self, value: str) -> Self:
        """Apply delta query

        Args:
            value (str): If unspecified, enumerates the hierarchy's current state. If latest, returns empty response
              with latest delta token. If a previous delta token, returns new state since that token.
        """
        self.query_options.custom["token"] = value
        return self

    @property
    def delta_token(self) -> Optional[str]:
        """The resumable delta token returned by the last delta query, if any.

        Extracted from the ``@odata.deltaLink`` URL so it can be passed straight
        back into :meth:`token` to resume the query.
        """
        return _extract_delta_token(self._delta_request_url)

    def set_property(self, name: str, value: Any, persist_changes: bool = False) -> Self:
        if name == self.context.pending_request().json_format.collection_delta:
            self._delta_request_url = value
        else:
            super().set_property(name, value, persist_changes)
        return self

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
        self.query_options.custom["$changeType"] = type_name.name
        return self

    @property
    def delta(self) -> DeltaCollection[ClientObjectT]:
        """
        Gets a new delta collection for tracking subsequent changes.

        This property implements the delta link pattern for tracking changes over time.
        The returned collection will only contain items that changed since the last request.

        Returns:
            DeltaCollection: A new collection configured for delta tracking
        """
        return self.properties.get(
            "delta",
            DeltaCollection(self.context, self._item_type, DeltaPath(self.resource_path)),
        )
