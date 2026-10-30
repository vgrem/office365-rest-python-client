from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class MacOSCustomConfiguration(Entity):
    @odata(name="payload")
    @property
    def payload(self) -> Optional[bytes]:
        """Gets the payload property"""
        return self.properties.get("payload", None)

    @odata(name="payloadFileName")
    @property
    def payload_file_name(self) -> Optional[str]:
        """Gets the payloadFileName property"""
        return self.properties.get("payloadFileName", None)

    @odata(name="payloadName")
    @property
    def payload_name(self) -> Optional[str]:
        """Gets the payloadName property"""
        return self.properties.get("payloadName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MacOSCustomConfiguration"
