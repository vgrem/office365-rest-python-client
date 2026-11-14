from __future__ import annotations

from uuid import UUID

from office365.security.alerts.evidence import AlertEvidence


class SecurityGroupEvidence(AlertEvidence):
    activeDirectoryObjectGuid: UUID | None = None
    displayName: str | None = None
    distinguishedName: str | None = None
    friendlyName: str | None = None
    securityGroupId: str | None = None
    sid: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SecurityGroupEvidence"
