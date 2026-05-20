from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.permissions.base_permissions import BasePermissions


@dataclass
class RoleDefinitionCreationInformation(ClientValue):
    """Contains properties that are used as parameters to initialize a role definition.

    :param str name: Specifies the name of the role definition.
    :param str description: Specifies the description of the role definition.
    :param int order: Specifies the order in which roles MUST be displayed in the WFE.
    """

    BasePermissions: BasePermissions = field(default_factory=BasePermissions)
    Name: Optional[str] = None
    Description: Optional[str] = None
    Order: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.RoleDefinition"
