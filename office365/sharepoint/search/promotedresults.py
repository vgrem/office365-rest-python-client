from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class PromotedResults(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        is_visual: Optional[bool] = None,
        last_modified_time: Optional[datetime] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.Description = description
        self.IsVisual = is_visual
        self.LastModifiedTime = last_modified_time
        self.Title = title
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResults"
