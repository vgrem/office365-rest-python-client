from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitescripts.action_status import SiteScriptActionStatus


@dataclass
class SPSiteScriptStatusAndSchema(ClientValue):
    ActionStatus: ClientValueCollection[SiteScriptActionStatus] = field(
        default_factory=lambda: ClientValueCollection(SiteScriptActionStatus)
    )
    Schema: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SPSiteScriptStatusAndSchema"
