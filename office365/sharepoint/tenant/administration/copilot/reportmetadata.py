from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class ReportMetadata(ClientValue):
    ReportMetadataDetails: dict = field(default_factory=dict)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportMetadata"
