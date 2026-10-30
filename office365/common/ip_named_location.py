from __future__ import annotations

from typing import Optional

from office365.directory.identities.ip_range import IpRange
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class IpNamedLocation(Entity):
    @odata(name="ipRanges")
    @property
    def ip_ranges(self) -> ClientValueCollection[IpRange]:
        """Gets the ipRanges property"""
        return self.properties.get("ipRanges", ClientValueCollection[IpRange](IpRange))

    @odata(name="isTrusted")
    @property
    def is_trusted(self) -> Optional[bool]:
        """Gets the isTrusted property"""
        return self.properties.get("isTrusted", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IpNamedLocation"
