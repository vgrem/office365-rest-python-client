from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union, cast

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.client_object import T
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class EntityCollection(ClientObjectCollection[T]):
    """A collection container which represents a named collections of entities"""

    def __init__(
        self,
        context: GraphClient,
        item_type: Type[T],
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[Entity] = None,
    ) -> None:
        super().__init__(context, item_type, resource_path, parent)
        self._delta_request_url = None

    def token(self, value: str) -> Self:
        """
        Apply delta query

        :param str value: If unspecified, enumerates the hierarchy's current state. If latest, returns empty
            response with latest delta token. If a previous delta token, returns new state since that token.
        """
        self.query_options.custom["token"] = value
        return self

    def __getitem__(self, key: Union[int, str]) -> T:
        """
        :param key: key is used to address an entity by either an index or by identifier
        :type key: int or str
        """
        if isinstance(key, int):
            return super().__getitem__(key)
        elif isinstance(key, str):
            return self.create_typed_object(resource_path=EntityPath(key, self.resource_path))
        else:
            raise ValueError("Invalid key: expected either an entity index [int] or identifier [str]")

    def add(self, **kwargs: Any) -> T:
        """Creates an entity and prepares the query"""
        return_type = self.create_typed_object(kwargs, EntityPath(None, self.resource_path))
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def create_typed_object(
        self,
        initial_properties: Optional[Dict] = None,
        resource_path: Optional[ResourcePath] = None,
    ) -> T:
        if resource_path is None:
            resource_path = EntityPath(None, self.resource_path)
        return super().create_typed_object(initial_properties, resource_path)

    def set_property(self, key: str, value: Any, persist_changes: bool = False) -> Self:
        if key == self.context.pending_request().json_format.collection_delta:
            self._delta_request_url = value
        else:
            super().set_property(key, value, persist_changes)
        return self

    @property
    def context(self) -> GraphClient:
        from office365.graph_client import GraphClient

        if self._context is None:
            raise ValueError("Graph client is not initialized")
        return cast(GraphClient, self._context)
