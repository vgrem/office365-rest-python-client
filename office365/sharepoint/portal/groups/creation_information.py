from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.groups.creation_params import GroupCreationParams


@dataclass
class GroupCreationInformation(ClientValue):
    displayName: str
    alias: str
    isPublic: bool
    optionalParams: GroupCreationParams = field(default_factory=GroupCreationParams)
    Description: str | None = None
    Title: str | None = None

    @property
    def entity_type_name(self):
        return None
