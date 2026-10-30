from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.print.printers.location import PrinterLocation
from office365.runtime.types.odata_property import odata


class PrintConnector(Entity):
    """Represents a print connector that has been registered by using a Universal Print subscription.
    The printConnector resource can be used to view connector status and update properties.
    """

    @odata(name="appVersion")
    @property
    def app_version(self) -> Optional[str]:
        """Gets the appVersion property"""
        return self.properties.get("appVersion", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="fullyQualifiedDomainName")
    @property
    def fully_qualified_domain_name(self) -> Optional[str]:
        """Gets the fullyQualifiedDomainName property"""
        return self.properties.get("fullyQualifiedDomainName", None)

    @odata(name="location")
    @property
    def location(self) -> PrinterLocation:
        """Gets the location property"""
        return self.properties.get("location", PrinterLocation())

    @odata(name="operatingSystem")
    @property
    def operating_system(self) -> Optional[str]:
        """Gets the operatingSystem property"""
        return self.properties.get("operatingSystem", None)

    @odata(name="registeredDateTime")
    @property
    def registered_date_time(self) -> Optional[datetime]:
        """Gets the registeredDateTime property"""
        return self.properties.get("registeredDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintConnector"
