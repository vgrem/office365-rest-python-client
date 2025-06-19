from dataclasses import dataclass


@dataclass(frozen=True)
class ClientCredential:
    """Represents client credentials for authentication.

    Attributes:
        client_id: The client identifier
        client_secret: The client secret key
    """

    client_id: str
    client_secret: str

    def __post_init__(self):
        """Validation."""
        if not self.client_id:
            raise ValueError("client_id cannot be empty")
        if not self.client_secret:
            raise ValueError("client_secret cannot be empty")
