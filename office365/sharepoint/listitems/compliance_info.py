from office365.runtime.client_value import ClientValue


class ListItemComplianceInfo(ClientValue):
    def __init__(
        self,
        compliance_tag: str = None,
        tag_policy_event_based: bool = None,
        tag_policy_hold: bool = None,
        tag_policy_record: bool = None,
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
