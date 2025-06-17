from enum import Enum


class GraphVersion(Enum):
    """Microsoft Graph API versions."""

    V1 = "v1.0"
    """Stable production version of Microsoft Graph API"""

    BETA = "beta"
    """Preview version with latest features (may change)"""

    @classmethod
    def default(cls) -> "GraphVersion":
        """Get the default stable version."""
        return cls.V1

    @property
    def is_stable(self) -> bool:
        """Check if this is a stable version."""
        return self == self.V1

    @property
    def is_beta(self) -> bool:
        """Check if this is the beta version."""
        return self == self.BETA
