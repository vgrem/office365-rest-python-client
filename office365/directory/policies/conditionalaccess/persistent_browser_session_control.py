from __future__ import annotations

from office365.directory.identities.conditional_access_session_control import ConditionalAccessSessionControl
from office365.directory.policies.persistentbrowsersessionmode import PersistentBrowserSessionMode


class PersistentBrowserSessionControl(ConditionalAccessSessionControl):
    mode: PersistentBrowserSessionMode = PersistentBrowserSessionMode.always

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PersistentBrowserSessionControl"
