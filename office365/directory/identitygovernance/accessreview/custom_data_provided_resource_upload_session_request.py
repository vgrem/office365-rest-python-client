from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.data import Data
from office365.runtime.client_value import ClientValue


class CustomDataProvidedResourceUploadSessionRequest(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomDataProvidedResourceUploadSessionRequest"

    data: Data = field(default_factory=Data)
