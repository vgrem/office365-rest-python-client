from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

@dataclass
class CustomExtensionOverwriteConfiguration(ClientValue):
    behaviorOnError: CustomExtensionBehaviorOnError = field(default_factory=CustomExtensionBehaviorOnError)
    clientConfiguration: CustomExtensionClientConfiguration = field(default_factory=CustomExtensionClientConfiguration)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.CustomExtensionOverwriteConfiguration'