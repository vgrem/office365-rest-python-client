from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AppliedConditionalAccessPolicy(ClientValue):
    """Indicates the attributes related to applied conditional access policy or policies that are triggered
    by a sign-in activity.

    The data in this object is returned only for callers with privileges to read conditional access data.
    For more information, see Permissions for viewing applied conditional access (CA) policies in sign-ins.
    """

    displayName: str | None = None
    enforcedGrantControls: StringCollection = field(default_factory=StringCollection)
    enforcedSessionControls: StringCollection = field(default_factory=StringCollection)
    id: str | None = None
    result: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppliedConditionalAccessPolicy"
