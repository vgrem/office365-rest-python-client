from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.audit.search_request_status import (
    AuditSearchRequestStatus,
)


@dataclass
class PageResponse(ClientValue):
    ContinuationToken: str | None = None
    PageNumber: int | None = None
    PageResult: ClientValueCollection[AuditSearchRequestStatus] = field(
        default_factory=lambda: ClientValueCollection(AuditSearchRequestStatus)
    )
    PageSize: int | None = None
    TotalCount: int | None = None
    TotalPages: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.PageResponse"
