from __future__ import annotations

from enum import Enum


class AccessPackageSubjectLifecycle(Enum):
    notDefined = "0"
    notGoverned = "1"
    governed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSubjectLifecycle"
