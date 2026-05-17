from office365.runtime.client_value import ClientValue
from typing import Optional


class UpdateWriteBackFileModel(ClientValue):
    def __init__(
        self,
        file_name: Optional[str] = None,
        list_item_id: Optional[str] = None,
        url: Optional[str] = None,
        work_item_id: Optional[str] = None,
    ):
        self.fileName = file_name
        self.listItemId = list_item_id
        self.url = url
        self.workItemId = work_item_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.UpdateWriteBackFileModel"
