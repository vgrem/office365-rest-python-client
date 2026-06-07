from office365.sharepoint.entity import Entity


class SPWorkflowManager(Entity):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "SP.Workflow.SPWorkflowManager"
