from __future__ import annotations

from enum import Enum


class AndroidManagedStoreAccountAppSyncStatus(Enum):
    success = "0"
    credentialsNotValid = "1"
    androidForWorkApiError = "2"
    managementServiceError = "3"
    unknownError = "4"
    none = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAccountAppSyncStatus"
