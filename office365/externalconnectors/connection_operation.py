from __future__ import annotations

from office365.entity import Entity
from office365.externalconnectors.connectionoperationstatus import ConnectionOperationStatus


class ConnectionOperation(Entity):
    @property
    def status(self) -> ConnectionOperationStatus:
        """Gets the status property"""
        return self.properties.get("status", ConnectionOperationStatus.unspecified)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ConnectionOperation"
