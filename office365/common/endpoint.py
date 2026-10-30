from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Endpoint(Entity):
    @odata(name="capability")
    @property
    def capability(self) -> Optional[str]:
        """Gets the capability property"""
        return self.properties.get("capability", None)

    @odata(name="providerId")
    @property
    def provider_id(self) -> Optional[str]:
        """Gets the providerId property"""
        return self.properties.get("providerId", None)

    @odata(name="providerName")
    @property
    def provider_name(self) -> Optional[str]:
        """Gets the providerName property"""
        return self.properties.get("providerName", None)

    @odata(name="providerResourceId")
    @property
    def provider_resource_id(self) -> Optional[str]:
        """Gets the providerResourceId property"""
        return self.properties.get("providerResourceId", None)

    @odata(name="uri")
    @property
    def uri(self) -> Optional[str]:
        """Gets the uri property"""
        return self.properties.get("uri", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Endpoint"
