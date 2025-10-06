from office365.runtime.client_value import ClientValue


class WebPartModel(ClientValue):

    def __init__(
        self,
        content: str = None,
        index: int = None,
        properties: dict = None,
        section_index: int = None,
        type_: str = None,
    ):
        self.content = content
        self.index = index
        self.properties = properties
        self.sectionIndex = section_index
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.WebPartModel"
