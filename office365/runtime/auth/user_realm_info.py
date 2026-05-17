from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserRealmInfo:
    """Represents user realm discovery information for authentication.

    Attributes:
        sts_auth_url: Security Token Service authentication URL (None for non-federated realms)
        is_federated: Indicates if the realm uses federated authentication
    """

    sts_auth_url: Optional[str]
    is_federated: bool

    def __str__(self) -> str:
        return f"Federated: {self.is_federated}, STS URL: {self.sts_auth_url}"
