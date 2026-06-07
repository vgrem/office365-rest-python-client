from office365.sharepoint.entity import Entity


class MicrofeedStore(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Microfeed.MicrofeedStore"
