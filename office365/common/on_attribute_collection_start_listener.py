from __future__ import annotations

from office365.directory.authentication.attributecollection.start_handler import OnAttributeCollectionStartHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnAttributeCollectionStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnAttributeCollectionStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnAttributeCollectionStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAttributeCollectionStartListener"
