from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AppleManagedIdentityProvider(Entity):
    @odata(name="certificateData")
    @property
    def certificate_data(self) -> Optional[str]:
        """Gets the certificateData property"""
        return self.properties.get("certificateData", None)

    @odata(name="developerId")
    @property
    def developer_id(self) -> Optional[str]:
        """Gets the developerId property"""
        return self.properties.get("developerId", None)

    @odata(name="keyId")
    @property
    def key_id(self) -> Optional[str]:
        """Gets the keyId property"""
        return self.properties.get("keyId", None)

    @odata(name="serviceId")
    @property
    def service_id(self) -> Optional[str]:
        """Gets the serviceId property"""
        return self.properties.get("serviceId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppleManagedIdentityProvider"
