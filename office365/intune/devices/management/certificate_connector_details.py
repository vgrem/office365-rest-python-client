from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class CertificateConnectorDetails(Entity):
    @odata(name="connectorName")
    @property
    def connector_name(self) -> Optional[str]:
        """Gets the connectorName property"""
        return self.properties.get("connectorName", None)

    @odata(name="connectorVersion")
    @property
    def connector_version(self) -> Optional[str]:
        """Gets the connectorVersion property"""
        return self.properties.get("connectorVersion", None)

    @odata(name="enrollmentDateTime")
    @property
    def enrollment_date_time(self) -> Optional[datetime]:
        """Gets the enrollmentDateTime property"""
        return self.properties.get("enrollmentDateTime", None)

    @odata(name="lastCheckinDateTime")
    @property
    def last_checkin_date_time(self) -> Optional[datetime]:
        """Gets the lastCheckinDateTime property"""
        return self.properties.get("lastCheckinDateTime", None)

    @odata(name="machineName")
    @property
    def machine_name(self) -> Optional[str]:
        """Gets the machineName property"""
        return self.properties.get("machineName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CertificateConnectorDetails"
