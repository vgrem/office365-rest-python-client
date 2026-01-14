from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.copilot.basemetadata import BaseMetadata


class BaseRawDataSources(ClientValue):
    def __init__(self, display_message: str = None, metadata: BaseMetadata = BaseMetadata()):
        self.DisplayMessage = display_message
        self.Metadata = metadata

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.BaseRawDataSources"
