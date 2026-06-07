from office365.sharepoint.entity import Entity


class WorkflowMessagingService(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.WorkflowServices.WorkflowMessagingService"
