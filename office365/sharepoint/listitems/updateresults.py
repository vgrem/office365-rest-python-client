from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.listitems.form_update_value import ListItemFormUpdateValue


class ListItemUpdateResults(ClientValue):
    def __init__(
        self,
        updated_data: str = None,
        update_results: ClientValueCollection[ListItemFormUpdateValue] = ClientValueCollection(ListItemFormUpdateValue),
    ):
        self.updated_data = updated_data
        self.update_results = update_results
