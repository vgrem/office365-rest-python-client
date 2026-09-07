from __future__ import annotations

from dataclasses import dataclass

from office365.directory.objects.object import DirectoryObject
from office365.runtime.client_value import ClientValue


@dataclass
class DirectoryObjectWorkflowSubject(ClientValue):
    directoryObject: DirectoryObject | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.DirectoryObjectWorkflowSubject"
