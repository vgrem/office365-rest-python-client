from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.header import Header
from typing import Optional


class MessageCardActionButton(ClientValue):
    def __init__(
        self,
        body: Optional[str] = None,
        body_content_type: Optional[str] = None,
        headers: ClientValueCollection[Header] = ClientValueCollection(Header),
        name: Optional[str] = None,
        target: Optional[str] = None,
        type_: Optional[str] = None,
    ):
        self.body = body
        self.bodyContentType = body_content_type
        self.headers = headers
        self.name = name
        self.target = target
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.MessageCardActionButton"
