from office365.sharepoint.entity import Entity


class PointPublishingTenantManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.PointPublishingTenantManager"
