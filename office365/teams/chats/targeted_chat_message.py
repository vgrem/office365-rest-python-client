from __future__ import annotations

from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TargetedChatMessage(Entity):
    @odata(name="recipient")
    @property
    def recipient(self) -> Identity:
        """Gets the recipient property"""
        return self.properties.get("recipient", Identity())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TargetedChatMessage"
