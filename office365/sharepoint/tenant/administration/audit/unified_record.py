from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.audit.data import AuditData


@dataclass
class UnifiedAuditRecord(ClientValue):
    AuditData: AuditData = field(default_factory=AuditData)
    CreationDate = None
    Operation = None
    RecordId = None
    RecordType = None
    UserId = None
    RawAuditData: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.UnifiedAuditRecord"
