from office365.sharepoint.entity import Entity


class NewsUtility(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Utilities.NewsUtility"
