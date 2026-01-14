from datetime import datetime

from office365.runtime.client_value import ClientValue


class PromotedResults(ClientValue):
    def __init__(
        self,
        description: str = None,
        is_visual: bool = None,
        last_modified_time: datetime = None,
        title: str = None,
        url: str = None,
    ):
        self.Description = description
        self.IsVisual = is_visual
        self.LastModifiedTime = last_modified_time
        self.Title = title
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResults"
