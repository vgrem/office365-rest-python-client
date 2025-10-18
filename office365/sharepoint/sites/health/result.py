from datetime import datetime

from office365.runtime.client_value import ClientValue


class SiteHealthResult(ClientValue):
    """Specifies the result of running a site collection sitehealth rule."""

    def __init__(
        self,
        message_as_text=None,
        rule_help_link=None,
        rule_id=None,
        rule_is_repairable: bool = None,
        rule_name: str = None,
        status: int = None,
        time_stamp: datetime = None,
    ):
        """
        :param str message_as_text: Specifies a summary of the results of running a site collection sitehealth rule.
        :param str rule_help_link: Specifies a hyperlink to help information about the site collection sitehealth rule.
        :param str rule_id: Specifies the unique identifier of the site collection sitehealth rule.
        """
        self.MessageAsText = message_as_text
        self.RuleHelpLink = rule_help_link
        self.RuleId = rule_id
        self.RuleIsRepairable = rule_is_repairable
        self.RuleName = rule_name
        self.Status = status
        self.TimeStamp = time_stamp

    @property
    def entity_type_name(self):
        return "SP.SiteHealth.SiteHealthResult"
