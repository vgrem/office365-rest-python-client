from office365.sharepoint.entity import Entity


class ApprovalsManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Internal.ApprovalsManager"
