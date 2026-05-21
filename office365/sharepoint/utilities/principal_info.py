from __future__ import annotations

from datetime import datetime
from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.principal.type import PrincipalType
from office365.sharepoint.sharing.ability_status import SharingAbilityStatus
from office365.sharepoint.sharing.inherited_from import InheritedFrom
from office365.sharepoint.sharing.principal import Principal


@dataclass
class PrincipalInfo(ClientValue):

    """
    Represents principal information.

    Provides comprehensive information about a SharePoint principal (user/group).
    Handles null values safely and provides type-safe access to principal properties.

    Example:
    >>> info = PrincipalInfo(display_name="John Doe", principal_type=PrincipalType.User)
    >>> print(info)  # "User: John Doe"
    """

    PrincipalId: Optional[str] = None
    DisplayName: Optional[str] = None
    Email: Optional[str] = None
    LoginName: Optional[str] = None
    Department: Optional[str] = None
    JobTitle: Optional[str] = None
    PrincipalType: Optional[PrincipalType] = None
    canBeModified: SharingAbilityStatus = SharingAbilityStatus()
    ExpirationDateTimeOnACE: Optional[datetime] = None
    inheritedFrom: InheritedFrom = InheritedFrom()
    isInherited: Optional[bool] = None
    members: ClientValueCollection[Principal] = ClientValueCollection(Principal)
    principal: Principal = Principal()
    role: Optional[int] = None
    Mobile: Optional[str] = None
    SIPAddress: Optional[str] = None

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