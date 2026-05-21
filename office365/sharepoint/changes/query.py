from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class ChangeQuery(ClientValue):

    """Defines a query that is performed against the change log."""

    Item = False
    Alert: bool = False
    ContentType = False
    Web = False
    Site: bool = False
    List = False
    Activity = False
    File = False
    Folder = False
    User = False
    Group = False
    View = False
    Add = True
    Update = True
    SystemUpdate = True
    ChangeTokenStart = None
    ChangeTokenEnd = None
    DeleteObject = True
    RoleAssignmentAdd = True
    RoleAssignmentDelete = True
    FetchLimit = None
    AppConsentPrincipal: Optional[bool] = None
    Field: Optional[bool] = None
    GroupMembershipAdd: Optional[bool] = None
    GroupMembershipDelete: Optional[bool] = None
    IgnoreStartTokenNotFoundError: Optional[bool] = None
    LatestFirst: Optional[bool] = None
    Move: Optional[bool] = None
    Navigation: Optional[bool] = None
    RecursiveAll: Optional[bool] = None
    Rename: Optional[bool] = None
    RequireSecurityTrim: Optional[bool] = None
    Restore: Optional[bool] = None
    RoleDefinitionAdd: Optional[bool] = None
    RoleDefinitionDelete: Optional[bool] = None
    RoleDefinitionUpdate: Optional[bool] = None
    SecurityPolicy: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.ChangeQuery"