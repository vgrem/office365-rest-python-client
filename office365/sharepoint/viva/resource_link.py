from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class VivaResourceLink(ClientValue):

    def __init__(
        self,
        audiences: StringCollection = StringCollection(),
        icon: str = None,
        id_: int = None,
        thumbnail_option: str = None,
        title: str = None,
        url: str = None,
    ):
        self.Audiences = audiences
        self.Icon = icon
        self.Id = id_
        self.ThumbnailOption = thumbnail_option
        self.Title = title
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.ResourceLink"
