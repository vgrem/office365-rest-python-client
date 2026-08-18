from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.guests_or_external_users import (
    ConditionalAccessGuestsOrExternalUsers,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ConditionalAccessUsers(ClientValue):
    excludeGroups: StringCollection = field(default_factory=StringCollection)
    excludeGuestsOrExternalUsers: ConditionalAccessGuestsOrExternalUsers = field(
        default_factory=ConditionalAccessGuestsOrExternalUsers
    )
    excludeRoles: StringCollection = field(default_factory=StringCollection)
    excludeUsers: StringCollection = field(default_factory=StringCollection)
    includeGroups: StringCollection = field(default_factory=StringCollection)
    includeGuestsOrExternalUsers: ConditionalAccessGuestsOrExternalUsers = field(
        default_factory=ConditionalAccessGuestsOrExternalUsers
    )
    includeRoles: StringCollection = field(default_factory=StringCollection)
    includeUsers: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessUsers"
