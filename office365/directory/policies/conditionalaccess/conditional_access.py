from datetime import datetime

from office365.entity import Entity


class ConditionalAccessPolicy(Entity):
    """
    Represents an Azure Active Directory conditional access policy.
    Conditional access policies are custom rules that define an access scenario.
    """

    @property
    def created_datetime(self) -> datetime:
        """Date and time (UTC) the sign-in was initiated."""
        return self.properties.get("createdDateTime", datetime.min)
