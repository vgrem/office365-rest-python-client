from enum import Enum


class TeamVisibilityType(Enum):
    """Describes the visibility of a team."""

    none_ = -1
    private = 0
    public = 1
    hiddenMembership = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamVisibilityType"
