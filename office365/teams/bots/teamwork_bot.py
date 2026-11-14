from office365.entity import Entity


class TeamworkBot(Entity):
    """Represents a bot in the Microsoft Teams ecosystem."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkBot"
