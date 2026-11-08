from __future__ import annotations

from office365.directory.authentication.attributecollection.handler import OnAttributeCollectionHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnAttributeCollectionListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnAttributeCollectionHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnAttributeCollectionHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAttributeCollectionListener"
