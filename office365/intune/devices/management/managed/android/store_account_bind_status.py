from __future__ import annotations

from enum import Enum


class AndroidManagedStoreAccountBindStatus(Enum):
    notBound = "0"
    bound = "1"
    boundAndValidated = "2"
    unbinding = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAccountBindStatus"
