from __future__ import annotations

from office365.directory.policies.persistentbrowsersessionmode import PersistentBrowserSessionMode
from office365.runtime.client_value import ClientValue


class PersistentBrowserSessionControl(ClientValue):
    mode: PersistentBrowserSessionMode = PersistentBrowserSessionMode.always

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PersistentBrowserSessionControl"
