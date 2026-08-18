from office365.entity import Entity


class UserSolutionRoot(Entity):
    """Represents an identifier that relates a user to the working time schedule triggers."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserSolutionRoot"
