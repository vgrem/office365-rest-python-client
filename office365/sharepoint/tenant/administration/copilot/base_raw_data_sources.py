from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.basemetadata import BaseMetadata


@dataclass
class BaseRawDataSources(ClientValue):
    DisplayMessage: str | None = None
    Metadata: BaseMetadata = field(default_factory=BaseMetadata)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.BaseRawDataSources"
