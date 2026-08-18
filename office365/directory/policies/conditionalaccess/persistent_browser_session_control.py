from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.persistentbrowsersessionmode import PersistentBrowserSessionMode
from office365.runtime.client_value import ClientValue


@dataclass
class PersistentBrowserSessionControl(ClientValue):
    mode: PersistentBrowserSessionMode = PersistentBrowserSessionMode.always

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PersistentBrowserSessionControl"
