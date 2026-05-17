from typing import Optional

from office365.runtime.client_value import ClientValue


class WebPartModel(ClientValue):
    def __init__(
        self,
        content: Optional[str] = None,
        index: Optional[int] = None,
        properties: Optional[dict] = None,
        section_index: Optional[int] = None,
        type_: Optional[str] = None,
    ):
        self.content = content
        self.index = index
        self.properties = properties
        self.sectionIndex = section_index
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.WebPartModel"
