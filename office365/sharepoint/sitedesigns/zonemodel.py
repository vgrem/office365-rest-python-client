from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.sectionmodel import SectionModel


class ZoneModel(ClientValue):

    def __init__(
        self,
        index: int = None,
        sections: ClientValueCollection[SectionModel] = ClientValueCollection(SectionModel),
    ):
        self.index = index
        self.sections = sections

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.ZoneModel"
