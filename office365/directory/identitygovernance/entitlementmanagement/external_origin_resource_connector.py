from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.connection_info import ConnectionInfo
    from office365.externalconnectors.connector_type import ConnectorType


class ExternalOriginResourceConnector(Entity):
    @odata(name="connectionInfo")
    @property
    def connection_info(self) -> ConnectionInfo:
        """Gets the connectionInfo property"""
        from office365.directory.connection_info import ConnectionInfo

        return self.properties.get("connectionInfo", ConnectionInfo())

    @odata(name="connectorType")
    @property
    def connector_type(self) -> Optional[ConnectorType]:
        """Gets the connectorType property"""
        return self.properties.get("connectorType", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="modifiedBy")
    @property
    def modified_by(self) -> Optional[str]:
        """Gets the modifiedBy property"""
        return self.properties.get("modifiedBy", None)

    @odata(name="modifiedDateTime")
    @property
    def modified_date_time(self) -> Optional[datetime]:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExternalOriginResourceConnector"
