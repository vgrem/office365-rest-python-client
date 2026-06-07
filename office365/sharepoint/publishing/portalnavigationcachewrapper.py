from office365.sharepoint.entity import Entity


class PortalNavigationCacheWrapper(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.Navigation.PortalNavigationCacheWrapper"
