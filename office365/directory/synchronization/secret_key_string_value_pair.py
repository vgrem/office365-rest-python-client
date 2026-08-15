from __future__ import annotations

from dataclasses import dataclass

from office365.directory.synchronization.secret import SynchronizationSecret
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationSecretKeyStringValuePair(ClientValue):
    key: SynchronizationSecret = SynchronizationSecret.None_
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationSecretKeyStringValuePair"
