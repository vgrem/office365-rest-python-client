from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamSummary(ClientValue):
    """Contains information about a team in Microsoft Teams, including number of owners, members, and guests.

    :param int guests_count: Count of guests in a team.
    :param int members_count: Count of members in a team.
    :param int owners_count: Count of owners in a team.
    """

    guestsCount: int | None = None
    membersCount: int | None = None
    ownersCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamSummary"
