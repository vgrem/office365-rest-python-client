from office365.sharepoint.entity import Entity


class SPOIdentityHelper(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SPO.Identity.SPOIdentityHelper"
