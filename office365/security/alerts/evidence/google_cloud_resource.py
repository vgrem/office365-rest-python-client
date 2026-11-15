from __future__ import annotations

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.googlecloudlocationtype import GoogleCloudLocationType


class GoogleCloudResourceEvidence(AlertEvidence):
    fullResourceName: str | None = None
    location: str | None = None
    locationType: GoogleCloudLocationType = GoogleCloudLocationType.unknown
    projectId: str | None = None
    projectNumber: int | None = None
    resourceName: str | None = None
    resourceType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.GoogleCloudResourceEvidence"
