from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemComplianceInfo(ClientValue):
    """
    :param str compliance_tag:
    :param bool tag_policy_event_based:
    :param bool tag_policy_hold:
    :param bool tag_policy_record:
    """

    ComplianceTag: str | None = None
    TagPolicyEventBased: bool | None = None
    TagPolicyHold: bool | None = None
    TagPolicyRecord: bool | None = None
