from __future__ import annotations

from enum import Enum


class AndroidManagedStoreAccountEnrollmentTarget(Enum):
    none = "0"
    all = "1"
    targeted = "2"
    targetedAsEnrollmentRestrictions = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAccountEnrollmentTarget"
