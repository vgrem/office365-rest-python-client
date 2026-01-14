from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class TeamAppInfo(ClientValue):
    def __init__(self, children: StringCollection = StringCollection(), name: str = None):
        self.Children = children
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.TeamAppInfo"
