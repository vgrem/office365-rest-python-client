from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class SPDeletedContainerProperties(ClientValue):
    ContainerId: str | None = None
    ContainerName: str | None = None
    CreatedOn: datetime | None = None
    DeletedOn: datetime | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDeletedContainerProperties"
