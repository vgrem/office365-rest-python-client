from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredential:
    """Credential container for username/password authentication.

     Attributes:
        userName: The username for authentication (typically email format)
        password: The password for authentication

    Example:
        >>> creds = UserCredential("user@example.com", "secure-password")
        >>> print(creds.userName)
        user@example.com
    """

    def __post_init__(self):
        """Basic validation."""
        if not self.userName:
            raise ValueError("Username cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")

    userName: str
    password: str
