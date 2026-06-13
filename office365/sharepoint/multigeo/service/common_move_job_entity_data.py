from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class CommonMoveJobEntityData(ClientValue):
    EnableRestoreOnSiteToMove: bool | None = None
    EnableSiteToMoveDatastore: bool | None = None
    GroupName: str | None = None
    HasOdbInSourceDataLocation: bool | None = None
    SourceCompanyId: UUID | None = None
    SourceInstanceId: UUID | None = None
    SourceMySiteHostUrl: str | None = None
    SourceSiteSubscriptionId: UUID | None = None
    SourceSiteUrl: str | None = None
    TargetCompanyId: UUID | None = None
    TargetFarmId: str | None = None
    TargetInstanceId: UUID | None = None
    TargetSiteSubscriptionId: UUID | None = None
    TargetSiteUrl: str | None = None
    TenantMergeSourceMySiteHostUrl: str | None = None
    TenantMergeTargetMySiteHostUrl: str | None = None
    UserPrincipalName: str | None = None
    ValidationResult: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CommonMoveJobEntityData"
