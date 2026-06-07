from office365.sharepoint.entity import Entity


class SPStartUtilitiesProxy(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SPStart.SPStartUtilitiesProxy"
