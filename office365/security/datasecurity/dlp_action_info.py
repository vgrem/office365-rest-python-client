from __future__ import annotations

from office365.directory.policies.dlpaction import DlpAction
from office365.runtime.client_value import ClientValue


class DlpActionInfo(ClientValue):
    action: DlpAction = DlpAction.notifyUser

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DlpActionInfo"
