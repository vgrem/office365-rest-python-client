from office365.entity import Entity


class UserStorage(Entity):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserStorage"
