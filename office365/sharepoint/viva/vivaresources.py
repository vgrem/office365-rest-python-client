from office365.sharepoint.entity import Entity


class VivaResources(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.EmployeeEngagement.VivaResources"
