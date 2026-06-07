from office365.sharepoint.entity import Entity


class WacApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Yammer.WacApi"
