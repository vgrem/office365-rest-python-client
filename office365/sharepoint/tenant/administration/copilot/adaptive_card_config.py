from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.base_raw_data_sources import (
    BaseRawDataSources,
)


@dataclass
class AdaptiveCardConfig(ClientValue):
    data: BaseRawDataSources = field(default_factory=BaseRawDataSources)
    featureName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.AdaptiveCardConfig"
