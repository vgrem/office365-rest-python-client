from __future__ import annotations

from enum import Enum


class TeamsAppInstallationScopes(Enum):
    team = "1"
    groupChat = "2"
    personal = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppInstallationScopes"
