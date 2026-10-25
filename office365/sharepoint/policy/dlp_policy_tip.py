from datetime import datetime
from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DlpPolicyTip(Entity):
    """Provides information about the Data Loss Protection policy on an item so it can be shown to the user."""

    @odata(name="AppliedActionsText")
    @property
    def applied_actions_text(self) -> Optional[str]:
        """Specifies the text which states what restrictive actions have been applied to this item."""
        return self.properties.get("AppliedActionsText", None)

    @odata(name="ComplianceUrl")
    @property
    def compliance_url(self) -> Optional[str]:
        """Specifies the URL that provides additional help on the policy tip dialog."""
        return self.properties.get("ComplianceUrl", None)

    @odata(name="GeneralText")
    @property
    def general_text(self) -> Optional[str]:
        """General text that appears on the top of the policy tip dialog."""
        return self.properties.get("GeneralText", None)

    @odata(name="LastProcessedTime")
    @property
    def last_processed_time(self) -> Optional[datetime]:
        """The last time this item was processed for policy matches."""
        return self.properties.get("LastProcessedTime", datetime.min)

    @odata(name="MatchedConditionDescriptions")
    @property
    def matched_condition_descriptions(self) -> StringCollection:
        """An array that contains a description of each policy condition that has been matched."""
        return self.properties.get("MatchedConditionDescriptions", StringCollection())

    @odata(name="OverrideOptions")
    @property
    def override_options(self) -> Optional[int]:
        """The allowable options that someone can take to override policy matches."""
        return self.properties.get("OverrideOptions", None)

    @odata(name="TwoLetterISOLanguageName")
    @property
    def two_letter_iso_language_name(self) -> Optional[str]:
        """The two-letter language code of the generated policy tip detail."""
        return self.properties.get("TwoLetterISOLanguageName", None)
