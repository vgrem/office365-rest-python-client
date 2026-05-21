from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.adaptive_card_config import (
    AdaptiveCardConfig,
)


@dataclass
class TranspilerResponse(ClientValue):
    config: AdaptiveCardConfig = field(default_factory=AdaptiveCardConfig)
    schemaVersion: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.TranspilerResponse"
