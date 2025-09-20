from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class CustomizedFormsPage(ClientValue):
    pass


class CustomizedFormsPageCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[CustomizedFormsPage] = ClientValueCollection(
            CustomizedFormsPage
        ),
    ):
        self.items = items
