from typing import Optional

from office365.runtime.client_value import ClientValue


class WriteBackLocationModel(ClientValue):
    def __init__(self, title: Optional[str] = None, uri: Optional[str] = None):
        self.title = title
        self.uri = uri

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.WriteBackLocationModel"
