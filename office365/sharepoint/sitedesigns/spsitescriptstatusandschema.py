from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.sitescripts.action_status import SiteScriptActionStatus


@value
class SPSiteScriptStatusAndSchema(ClientValue):
    ActionStatus: ClientValueCollection[SiteScriptActionStatus] = field(
        default_factory=lambda: ClientValueCollection(SiteScriptActionStatus)
    )
    Schema: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SPSiteScriptStatusAndSchema"
