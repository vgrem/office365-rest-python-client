from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemComplianceInfo(ClientValue):
    """Args:
        compliance_tag (str):
        tag_policy_event_based (bool):
        tag_policy_hold (bool):
        tag_policy_record (bool):
    """

    ComplianceTag: str | None = None
    TagPolicyEventBased: bool | None = None
    TagPolicyHold: bool | None = None
    TagPolicyRecord: bool | None = None
