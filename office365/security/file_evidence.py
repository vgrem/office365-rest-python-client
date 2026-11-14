from __future__ import annotations

from dataclasses import field

from office365.security.alerts.detectionstatus import DetectionStatus
from office365.security.alerts.evidence import AlertEvidence
from office365.security.file_details import FileDetails


class FileEvidence(AlertEvidence):
    detectionStatus: DetectionStatus = DetectionStatus.detected
    fileDetails: FileDetails = field(default_factory=FileDetails)
    mdeDeviceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileEvidence"
