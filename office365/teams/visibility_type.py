from enum import Enum


class TeamVisibilityType(Enum):
    """Describes the visibility of a team."""

    none_ = -1
    private = 0
    public = 1
