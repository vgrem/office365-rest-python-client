from typing import Optional

from office365.entity import Entity


class UserInsightsSettings(Entity):
    """
    Represents user privacy settings for itemInsights and meeting hours insights. Use this resource to enable
    or disable the calculation and visibility of item insights and meeting hours insights for a user.

    Item insights: Calculates the relationships between users and items such as documents or sites in Microsoft 365.
    Meeting hours insights: Calculates a person's calendar meeting hours based on activities in
    Word, Excel, PowerPoint, email, and Outlook calendar in Microsoft 365.

    Use the insightsSettings resource to enable or disable the calculation and visibility of item insights,
    meeting hours insights, and people insights at the organizational level.
    """

    @property
    def is_enabled(self) -> Optional[bool]:
        """True if the user's itemInsights and meeting hours insights are enabled; false if the user's itemInsights
        and meeting hours insights are disabled. The default value is true. Optional."""
        return self.properties.get("isEnabled", None)
