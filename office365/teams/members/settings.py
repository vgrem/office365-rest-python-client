from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TeamMemberSettings(ClientValue):
    """Settings to configure whether members can perform certain actions, for example, create channels and add bots,
    in the team."""

    allowCreateUpdateChannels: bool | None = None
    allowDeleteChannels: bool = True
    allowAddRemoveApps: bool = True
    allowCreateUpdateRemoveTabs: bool = True
    allowCreateUpdateRemoveConnectors: bool = True
