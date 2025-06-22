from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.type import PrincipalType


class PrincipalInfo(ClientValue):
    """Represents principal information.

    Provides comprehensive information about a SharePoint principal (user/group).
    Handles null values safely and provides type-safe access to principal properties.

    Example:
        >>> info = PrincipalInfo(display_name="John Doe", principal_type=PrincipalType.User)
        >>> print(info)  # "User: John Doe"
    """

    def __init__(
        self,
        principal_id: str = None,
        display_name: str = None,
        email: str = None,
        login_name: str = None,
        department: str = None,
        job_title: str = None,
        principal_type: PrincipalType = None,
    ):
        """Initialize principal information.

        Args:
            principal_id: Unique identifier (-1 if external to site)
            display_name: Human-readable display name
            email: Email address
            login_name: System login identifier
            department: Organizational department
            job_title: Job position title
            principal_type: Type of principal (User/Group/etc)
        """
        self.PrincipalId = principal_id
        self.DisplayName = display_name
        self.Email = email
        self.LoginName = login_name
        self.Department = department
        self.JobTitle = job_title
        self.PrincipalType = principal_type

    @property
    def entity_type_name(self):
        return "SP.Utilities.PrincipalInfo"

    @property
    def principal_type_name(self):
        """Gets the string name of the principal type if available.

        Returns:
            The principal type name or None if not set
        """
        return getattr(self.PrincipalType, "name", None)

    def __str__(self):
        """Human-readable representation of the principal.

        Returns:
            String in format "{Type}: {Name}" or "Unknown Principal" if minimal data
        """
        type_name = self.principal_type_name or "Unknown"
        name = self.DisplayName or "Principal"
        return f"{type_name}: {name}"
