from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TeamworkActivityTopic(ClientValue):
    """Represents the topic of an activity feed notification."""

    source: str | None = None
    value: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkActivityTopic"
