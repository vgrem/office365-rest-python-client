from __future__ import annotations

from office365.security.alerts.evidence import AlertEvidence


class RegistryValueEvidence(AlertEvidence):
    mdeDeviceId: str | None = None
    registryHive: str | None = None
    registryKey: str | None = None
    registryValue: str | None = None
    registryValueName: str | None = None
    registryValueType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RegistryValueEvidence"
