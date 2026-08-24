from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPOFileArchivePolicyReportInfo(ClientValue):
    CompleteDate: datetime | None = field(default_factory=lambda: datetime.min)
    FilesArchivedCount: int | None = None
    FilesEligibleForArchiveCount: int | None = None
    GBsArchived: float | None = None
    GBsEligibleForArchive: float | None = None
    SiteProcessedCount: int | None = None
    WhatIfMode: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileArchivePolicyReportInfo"
