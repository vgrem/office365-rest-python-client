from office365.runtime.client_value import ClientValue


class WorkflowAssociationCreationInformation(ClientValue):
    def __init__(
        self,
        content_type_association_history_list_name: str = None,
        content_type_association_task_list_name: str = None,
        name: str = None,
    ):
        self.ContentTypeAssociationHistoryListName = content_type_association_history_list_name
        self.ContentTypeAssociationTaskListName = content_type_association_task_list_name
        self.Name = name

    @property
    def entity_type_name(self):
        return "SP.Workflow.WorkflowAssociationCreationInformation"
