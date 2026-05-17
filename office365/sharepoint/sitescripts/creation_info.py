from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteScriptCreationInfo(ClientValue):
    def __init__(self, content: Optional[str] = None, description: Optional[str] = None, title: Optional[str] = None):
        self.Content = content
        self.Description = description
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptCreationInfo"
