from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.subjectset import SubjectSet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageAssignmentRequestorSettings(ClientValue):
    allowCustomAssignmentSchedule: bool | None = None
    enableOnBehalfRequestorsToAddAccess: bool | None = None
    enableOnBehalfRequestorsToRemoveAccess: bool | None = None
    enableOnBehalfRequestorsToUpdateAccess: bool | None = None
    enableTargetsToSelfAddAccess: bool | None = None
    enableTargetsToSelfRemoveAccess: bool | None = None
    enableTargetsToSelfUpdateAccess: bool | None = None
    onBehalfRequestors: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequestorSettings"
