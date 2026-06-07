from office365.sharepoint.entity import Entity


class SPAppStateQueryJobDefinition(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.SPAppStateQueryJobDefinition"
