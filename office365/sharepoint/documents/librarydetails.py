from office365.runtime.client_value import ClientValue
from typing import Optional


class LibraryDetails(ClientValue):
    def __init__(
        self,
        base_template_type: Optional[int] = None,
        is_approvals_enabled: Optional[bool] = None,
        list_id: Optional[str] = None,
        list_item_entity_type_full_name: Optional[str] = None,
        list_name: Optional[str] = None,
    ):
        self.BaseTemplateType = base_template_type
        self.IsApprovalsEnabled = is_approvals_enabled
        self.ListId = list_id
        self.ListItemEntityTypeFullName = list_item_entity_type_full_name
        self.ListName = list_name
