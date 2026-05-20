from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.autoinvokeaction import AutoInvokeAction
from office365.sharepoint.sitedesigns.autoinvokeoptions import AutoInvokeOptions
from office365.sharepoint.sitedesigns.potentialaction import PotentialAction
from office365.sharepoint.sitedesigns.section import Section


@dataclass
class MessageCard(ClientValue):
    autoInvokeAction: AutoInvokeAction = field(default_factory=AutoInvokeAction)
    autoInvokeOptions: AutoInvokeOptions = field(default_factory=AutoInvokeOptions)
    context: Optional[str] = None
    hideOriginalBody: Optional[str] = None
    originator: Optional[str] = None
    potentialAction: ClientValueCollection[PotentialAction] = field(
        default_factory=lambda: ClientValueCollection(PotentialAction)
    )
    sections: ClientValueCollection[Section] = field(default_factory=lambda: ClientValueCollection(Section))
    text: Optional[str] = None
    themeColor: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCard"
