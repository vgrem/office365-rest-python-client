from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class OdbLicenseUpdatedUserDetail(ClientValue):
    IsLicenseAdded: bool | None = None
    IsLicenseRemoved: bool | None = None
    LicenseUpdateTime: datetime | None = field(default_factory=lambda: datetime.min)
    MySiteHostUrl: str | None = None
    TenantCompanyId: UUID | None = None
    TenantInstanceId: UUID | None = None
    UserObjectId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.Service.OdbLicenseUpdatedUserDetail"
