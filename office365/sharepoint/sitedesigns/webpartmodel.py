from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WebPartModel(ClientValue):
    content: Optional[str] = None
    index: Optional[int] = None
    properties: Optional[dict] = None
    sectionIndex: Optional[int] = None
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.WebPartModel"
