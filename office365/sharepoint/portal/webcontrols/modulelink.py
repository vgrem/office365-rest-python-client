from office365.sharepoint.entity import Entity


class ModuleLink(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.WebControls.ModuleLink"
