from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.audit.data import AuditData


@dataclass
class UnifiedAuditRecord(ClientValue):
    AuditData: AuditData = field(default_factory=AuditData)
    RawAuditData: str | None = None
    CreationDate: datetime | None = field(default_factory=lambda: datetime.min)
    Operation: str | None = None
    RecordId: UUID | None = None
    RecordType: int | None = None
    UserId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.UnifiedAuditRecord"
