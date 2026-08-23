from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.notify_members import NotifyMembers
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class TargetOwners(ClientValue):
    notifyMembers: NotifyMembers = NotifyMembers.all
    securityGroups: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TargetOwners"
