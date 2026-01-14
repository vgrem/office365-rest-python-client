from office365.runtime.client_value import ClientValue


class UpdateWriteBackFileModel(ClientValue):
    def __init__(
        self,
        file_name: str = None,
        list_item_id: str = None,
        url: str = None,
        work_item_id: str = None,
    ):
        self.fileName = file_name
        self.listItemId = list_item_id
        self.url = url
        self.workItemId = work_item_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.UpdateWriteBackFileModel"
