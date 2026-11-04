from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPJitDlpPolicyData(ClientValue):
    ExecutionMode: Optional[int] = None
    IsPolicyEnabled: Optional[bool] = None
    ODBSensitivityRefreshWindowInHours: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.SPJitDlpPolicyData"
