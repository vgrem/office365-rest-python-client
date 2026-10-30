from __future__ import annotations

from office365.directory.authentication.attributecollection.submit_handler import OnAttributeCollectionSubmitHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnAttributeCollectionSubmitListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnAttributeCollectionSubmitHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnAttributeCollectionSubmitHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAttributeCollectionSubmitListener"
