from office365.runtime.client_value import ClientValue


class SiteScriptCreationInfo(ClientValue):

    def __init__(self, content: str = None, description: str = None, title: str = None):
        self.Content = content
        self.Description = description
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptCreationInfo"
