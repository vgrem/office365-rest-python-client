from __future__ import annotations

from office365.directory.identities.on_user_create_start_handler import OnUserCreateStartHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnUserCreateStartListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnUserCreateStartHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnUserCreateStartHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnUserCreateStartListener"
