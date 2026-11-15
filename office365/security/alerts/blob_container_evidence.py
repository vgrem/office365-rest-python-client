from __future__ import annotations

from dataclasses import field

from office365.security.alerts.azure_resource_evidence import AzureResourceEvidence
from office365.security.alerts.evidence.base import AlertEvidence


class BlobContainerEvidence(AlertEvidence):
    name: str | None = None
    storageResource: AzureResourceEvidence = field(default_factory=AzureResourceEvidence)
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.BlobContainerEvidence"
