from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.autoinvokeaction import AutoInvokeAction
from office365.sharepoint.sitedesigns.autoinvokeoptions import AutoInvokeOptions
from office365.sharepoint.sitedesigns.potentialaction import PotentialAction
from office365.sharepoint.sitedesigns.section import Section


class MessageCard(ClientValue):
    def __init__(
        self,
        auto_invoke_action: AutoInvokeAction = AutoInvokeAction(),
        auto_invoke_options: AutoInvokeOptions = AutoInvokeOptions(),
        context: str = None,
        hide_original_body: str = None,
        originator: str = None,
        potential_action: ClientValueCollection[PotentialAction] = ClientValueCollection(PotentialAction),
        sections: ClientValueCollection[Section] = ClientValueCollection(Section),
        text: str = None,
        theme_color: str = None,
        title: str = None,
        type_: str = None,
    ):
        self.autoInvokeAction = auto_invoke_action
        self.autoInvokeOptions = auto_invoke_options
        self.context = context
        self.hideOriginalBody = hide_original_body
        self.originator = originator
        self.potentialAction = potential_action
        self.sections = sections
        self.text = text
        self.themeColor = theme_color
        self.title = title
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCard"
