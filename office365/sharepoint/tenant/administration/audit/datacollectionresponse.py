from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPAuditDataCollectionResponse(ClientValue):
    DataCollectionStatus: int | None = None
    OptInDateTime: datetime | None = None
    OptOutDateTime: datetime | None = None
    ReportEntity: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPAuditDataCollectionResponse"
