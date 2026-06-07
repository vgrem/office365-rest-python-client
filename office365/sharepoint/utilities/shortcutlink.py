from office365.sharepoint.entity import Entity


class ShortcutLink(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Utilities.ShortcutLink"
