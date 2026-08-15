from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.synchronization.job_subject import SynchronizationJobSubject
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class SynchronizationJobApplicationParameters(ClientValue):
    ruleId: str | None = None
    subjects: ClientValueCollection[SynchronizationJobSubject] = field(
        default_factory=lambda: ClientValueCollection(SynchronizationJobSubject)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationJobApplicationParameters"
