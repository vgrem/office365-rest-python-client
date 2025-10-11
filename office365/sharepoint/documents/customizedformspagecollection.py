from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.customizedformspage import CustomizedFormsPage


class CustomizedFormsPageCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[CustomizedFormsPage] = ClientValueCollection(CustomizedFormsPage),
    ):
        self.items = items
