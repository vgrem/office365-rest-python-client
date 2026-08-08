from typing import Optional

from office365.directory.policies.base import PolicyBase


class IdentitySecurityDefaultsEnforcementPolicy(PolicyBase):
    """Represents the Microsoft Entra security defaults policy.

    Security defaults enable common identity security protections across the tenant.
    It's a singleton policy that can be either enabled or disabled.
    """

    @property
    def is_enabled(self) -> Optional[bool]:
        """If set to true, security defaults are enabled for the tenant."""
        return self.properties.get("isEnabled", None)
