from office365.runtime.client_value import ClientValue


class LibraryDetails(ClientValue):
    def __init__(
        self,
        base_template_type: int = None,
        is_approvals_enabled: bool = None,
        list_id: str = None,
        list_item_entity_type_full_name: str = None,
        list_name: str = None,
    ):
        self.BaseTemplateType = base_template_type
        self.IsApprovalsEnabled = is_approvals_enabled
        self.ListId = list_id
        self.ListItemEntityTypeFullName = list_item_entity_type_full_name
        self.ListName = list_name
