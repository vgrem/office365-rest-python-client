from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class GovernanceHub(ClientValue):
    executionIdentifiers: str | None = None
    lastActionedOn: datetime | None = field(default_factory=lambda: datetime.min)
    lastEmailSentOn: datetime | None = field(default_factory=lambda: datetime.min)
    lastVisitedOn: datetime | None = field(default_factory=lambda: datetime.min)
    resourceDetails: str | None = None
    updatedOn: datetime | None = field(default_factory=lambda: datetime.min)
    userId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.GovernanceHub"
