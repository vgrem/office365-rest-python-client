from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.azure_resource_evidence import AzureResourceEvidence
from office365.runtime.client_value import ClientValue


@dataclass
class BlobContainerEvidence(ClientValue):
    name: str | None = None
    storageResource: AzureResourceEvidence = field(default_factory=AzureResourceEvidence)
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.BlobContainerEvidence"
