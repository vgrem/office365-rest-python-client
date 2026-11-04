from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.directory.synchronization.job_subject import SynchronizationJobSubject


@value
class SynchronizationLinkedObjects(ClientValue):
    manager: SynchronizationJobSubject | None = None
    members: ClientValueCollection[SynchronizationJobSubject] | None = None
    owners: ClientValueCollection[SynchronizationJobSubject] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationLinkedObjects"
