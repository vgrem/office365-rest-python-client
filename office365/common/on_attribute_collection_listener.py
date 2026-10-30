from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.attributecollection.handler import (
        OnAttributeCollectionHandler,
    )


class OnAttributeCollectionListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnAttributeCollectionHandler:
        """Gets the handler property"""
        from office365.directory.authentication.attributecollection.handler import (
            OnAttributeCollectionHandler,
        )

        return self.properties.get("handler", OnAttributeCollectionHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAttributeCollectionListener"
