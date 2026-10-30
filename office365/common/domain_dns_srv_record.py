from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DomainDnsSrvRecord(Entity):
    @odata(name="nameTarget")
    @property
    def name_target(self) -> Optional[str]:
        """Gets the nameTarget property"""
        return self.properties.get("nameTarget", None)

    @odata(name="port")
    @property
    def port(self) -> Optional[int]:
        """Gets the port property"""
        return self.properties.get("port", None)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[int]:
        """Gets the priority property"""
        return self.properties.get("priority", None)

    @odata(name="protocol")
    @property
    def protocol(self) -> Optional[str]:
        """Gets the protocol property"""
        return self.properties.get("protocol", None)

    @odata(name="service")
    @property
    def service(self) -> Optional[str]:
        """Gets the service property"""
        return self.properties.get("service", None)

    @odata(name="weight")
    @property
    def weight(self) -> Optional[int]:
        """Gets the weight property"""
        return self.properties.get("weight", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DomainDnsSrvRecord"
