from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class VivaResourceLink(ClientValue):
    def __init__(
        self,
        audiences: StringCollection = StringCollection(),
        icon: Optional[str] = None,
        id_: Optional[int] = None,
        thumbnail_option: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
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
