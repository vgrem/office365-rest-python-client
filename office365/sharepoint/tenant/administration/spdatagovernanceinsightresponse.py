from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class SPDataGovernanceInsightResponse(ClientValue):
    CountOfSitesInReport: int | None = None
    CountOfSitesInReportUserPermissions: int | None = None
    CountOfSitesInTenant: int | None = None
    CountOfSitesInTenantUserPermissions: int | None = None
    CreatedDateTime: str | None = None
    EEEUType: str | None = None
    InvalidUserEntries: StringCollection = field(default_factory=lambda: StringCollection())
    LabelId: UUID | None = None
    LabelName: str | None = None
    PrivacyEEEU: StringCollection = field(default_factory=lambda: StringCollection())
    PrivacySitePermissions: str | None = None
    ReportEndTimeEEEU: str | None = None
    ReportEndTimeSharingLink: str | None = None
    ReportEntity: str | None = None
    ReportFormat: str | None = None
    ReportId: UUID | None = None
    ReportNameEEEU: str | None = None
    ReportNameSitePermissions: str | None = None
    ReportNameUserPermissions: str | None = None
    ReportStartTimeEEEU: str | None = None
    ReportStartTimeSharingLink: str | None = None
    ReportType: str | None = None
    SensitivityEEEU: StringCollection = field(default_factory=lambda: StringCollection())
    SensitivitySitePermissions: StringCollection = field(default_factory=lambda: StringCollection())
    SharingLinkType: str | None = None
    SitesFoundEEEU: int | None = None
    SitesFoundSharingLink: int | None = None
    Status: str | None = None
    TemplatesEEEU: StringCollection = field(default_factory=lambda: StringCollection())
    TemplatesSitePermissions: StringCollection | None = None
    TriggeredDateTime: str | None = None
    UserEmailList: StringCollection = field(default_factory=lambda: StringCollection())
    UserID: UUID | None = None
    UserIDList: GuidCollection = field(default_factory=GuidCollection)
    UserLimit: int | None = None
    Variation: str | None = None
    Version: str | None = None
    Workload: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightResponse"
