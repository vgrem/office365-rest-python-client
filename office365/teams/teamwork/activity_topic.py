from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamworkActivityTopic(ClientValue):
    """Represents the topic of an activity feed notification."""

    source: str | None = None
    value: str | None = None
    webUrl: str | None = None
