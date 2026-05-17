from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.adaptive_card_config import (
    AdaptiveCardConfig,
)
from typing import Optional


class TranspilerResponse(ClientValue):
    def __init__(
        self,
        config: AdaptiveCardConfig = AdaptiveCardConfig(),
        schema_version: Optional[str] = None,
    ):
        self.config = config
        self.schemaVersion = schema_version

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.TranspilerResponse"
