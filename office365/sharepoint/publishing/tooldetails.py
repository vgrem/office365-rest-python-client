from typing import Optional

from office365.runtime.client_value import ClientValue


class ToolDetails(ClientValue):
    def __init__(self, name: Optional[str] = None, version: Optional[str] = None):
        self.Name = name
        self.Version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.ToolDetails"
