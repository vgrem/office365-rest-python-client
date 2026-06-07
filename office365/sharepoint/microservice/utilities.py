from office365.sharepoint.entity import Entity


class MicroServiceUtilities(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.MicroService.MicroServiceUtilities"
