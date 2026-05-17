from typing import Optional

from office365.runtime.client_value import ClientValue


class ListItemComplianceInfo(ClientValue):
    def __init__(
        self,
        compliance_tag: Optional[str] = None,
        tag_policy_event_based: Optional[bool] = None,
        tag_policy_hold: Optional[bool] = None,
        tag_policy_record: Optional[bool] = None,
    ):
        """
        :param str compliance_tag:
        :param bool tag_policy_event_based:
        :param bool tag_policy_hold:
        :param bool tag_policy_record:
        """
        self.ComplianceTag = compliance_tag
        self.TagPolicyEventBased = tag_policy_event_based
        self.TagPolicyHold = tag_policy_hold
        self.TagPolicyRecord = tag_policy_record
