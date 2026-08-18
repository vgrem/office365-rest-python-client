from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.deviceplatform import ConditionalAccessDevicePlatform
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ConditionalAccessPlatforms(ClientValue):
    excludePlatforms: ClientValueCollection[ConditionalAccessDevicePlatform] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessDevicePlatform)
    )
    includePlatforms: ClientValueCollection[ConditionalAccessDevicePlatform] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessDevicePlatform)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessPlatforms"
