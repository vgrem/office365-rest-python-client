from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.base_raw_data_sources import (
    BaseRawDataSources,
)


class AdaptiveCardConfig(ClientValue):
    def __init__(self, data: BaseRawDataSources = BaseRawDataSources(), feature_name: Optional[str] = None):
        self.data = data
        self.featureName = feature_name

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.AdaptiveCardConfig"
