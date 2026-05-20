from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SpotlightNews(ClientValue):
    AltText: Optional[str] = None
    ImageUrl: Optional[str] = None
    IsBoosted: Optional[bool] = None
    Order: Optional[int] = None
    Title: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.SpotlightNews"
