from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AuthorizationInfo(ClientValue):
    certificateUserIds: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthorizationInfo"
