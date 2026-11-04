from __future__ import annotations

from dataclasses import field

from office365.directory.identities.ip_range import IpRange
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class WindowsInformationProtectionIPRangeCollection(ClientValue):
    displayName: str | None = None
    ranges: ClientValueCollection[IpRange] = field(default_factory=lambda: ClientValueCollection(IpRange))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionIPRangeCollection"
