from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class LastAccessDateReportPackageResult(ClientValue):
    Detail: str | None = None
    IncludedSiteCount: int | None = None
    IndexServerRelativeUrl: str | None = None
    MissingSiteCount: int | None = None
    RunId: UUID | None = None
    ServerRelativeUrl: str | None = None
    Sha256: str | None = None
    SiteCount: int | None = None
    SizeBytes: int | None = None
    State: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.LastAccessDateReportPackageResult"
