from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.base_raw_data_sources import (
    BaseRawDataSources,
)


class AdaptiveCardConfig(ClientValue):

    def __init__(self, data: BaseRawDataSources = BaseRawDataSources(), feature_name: str = None):
        self.data = data
        self.featureName = feature_name

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.AdaptiveCardConfig"
