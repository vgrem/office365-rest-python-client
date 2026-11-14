from office365.entity import Entity


class AIInteractionHistory(Entity):
    """Represents a list of messages that are exchanged and involve AI."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionHistory"
