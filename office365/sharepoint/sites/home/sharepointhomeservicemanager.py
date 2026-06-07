from office365.sharepoint.entity import Entity


class SharePointHomeServiceManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.SharePointHomeServiceManager"
