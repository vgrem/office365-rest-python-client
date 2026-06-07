from office365.sharepoint.entity import Entity


class EntityFieldValueDictionary(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.BusinessData.Runtime.EntityFieldValueDictionary"
