from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class VivaResourceLink(ClientValue):
    Audiences: StringCollection = field(default_factory=StringCollection)
    Icon: Optional[str] = None
    Id: Optional[int] = None
    ThumbnailOption: Optional[str] = None
    Title: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.ResourceLink"
