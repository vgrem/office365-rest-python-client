from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.synchronization.linked_objects import SynchronizationLinkedObjects
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationJobSubject(ClientValue):
    links: SynchronizationLinkedObjects = field(default_factory=SynchronizationLinkedObjects)
    objectId: str | None = None
    objectTypeName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationJobSubject"
