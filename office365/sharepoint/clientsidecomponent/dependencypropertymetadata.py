from office365.sharepoint.entity import Entity


class DependencyPropertyMetadata(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ClientSideComponent.DependencyPropertyMetadata"
