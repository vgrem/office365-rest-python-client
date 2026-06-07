from office365.sharepoint.entity import Entity


class ExternalSubscriptionStore(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.BusinessData.Infrastructure.ExternalSubscriptionStore"
