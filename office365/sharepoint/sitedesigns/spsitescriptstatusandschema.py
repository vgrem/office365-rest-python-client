from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitescripts.action_status import SiteScriptActionStatus


class SPSiteScriptStatusAndSchema(ClientValue):

    def __init__(
        self,
        action_status: ClientValueCollection[
            SiteScriptActionStatus
        ] = ClientValueCollection(SiteScriptActionStatus),
        schema: str = None,
    ):
        self.ActionStatus = action_status
        self.Schema = schema

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SPSiteScriptStatusAndSchema"
