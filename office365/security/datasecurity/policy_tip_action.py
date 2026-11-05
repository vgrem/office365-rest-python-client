from __future__ import annotations

from office365.security.datasecurity.dlp_action_info import DlpActionInfo


class PolicyTipAction(DlpActionInfo):
    complianceUrl: str | None = None
    matchedConditionsDescription: str | None = None
    policyTip: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicyTipAction"
