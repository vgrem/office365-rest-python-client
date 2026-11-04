from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.alerts.detectionstatus import DetectionStatus
from office365.security.file_details import FileDetails


@value
class FileEvidence(ClientValue):
    detectionStatus: DetectionStatus = DetectionStatus.detected
    fileDetails: FileDetails = field(default_factory=FileDetails)
    mdeDeviceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileEvidence"
