from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.alerts.iotdeviceimportancetype import IoTDeviceImportanceType
from office365.directory.security.azure_resource_evidence import AzureResourceEvidence
from office365.directory.security.ip_evidence import IpEvidence
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class IoTDeviceEvidence(ClientValue):
    deviceId: str | None = None
    deviceName: str | None = None
    devicePageLink: str | None = None
    deviceSubType: str | None = None
    deviceType: str | None = None
    importance: IoTDeviceImportanceType = IoTDeviceImportanceType.unknown
    ioTHub: AzureResourceEvidence = field(default_factory=AzureResourceEvidence)
    ioTSecurityAgentId: str | None = None
    ipAddress: IpEvidence = field(default_factory=IpEvidence)
    isAuthorized: bool | None = None
    isProgramming: bool | None = None
    isScanner: bool | None = None
    macAddress: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    operatingSystem: str | None = None
    owners: StringCollection = field(default_factory=StringCollection)
    protocols: StringCollection = field(default_factory=StringCollection)
    purdueLayer: str | None = None
    sensor: str | None = None
    serialNumber: str | None = None
    site: str | None = None
    source: str | None = None
    zone: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IoTDeviceEvidence"
