from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.runtime.paths.resource_path import ResourcePath

@dataclass
class FraudProtectionProviderConfiguration(ClientValue):
    fraudProtectionProvider: FraudProtectionProvider | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.FraudProtectionProviderConfiguration'