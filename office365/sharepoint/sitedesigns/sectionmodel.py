from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.webpartmodel import WebPartModel


class SectionModel(ClientValue):

    def __init__(
        self,
        index: int = None,
        web_parts: ClientValueCollection[WebPartModel] = ClientValueCollection(
            WebPartModel
        ),
    ):
        self.index = index
        self.webParts = web_parts

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.SectionModel"
