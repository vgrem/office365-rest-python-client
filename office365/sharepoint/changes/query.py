from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ChangeQuery(ClientValue):
    """Defines a query that is performed against the change log."""

    Item: bool = False
    Alert: bool = False
    ContentType: bool = False
    Web: bool = False
    Site: bool = False
    List: bool = False
    Activity: bool = False
    File: bool = False
    Folder: bool = False
    User: bool = False
    Group: bool = False
    View: bool = False
    Add: bool = True
    Update: bool = True
    SystemUpdate: bool = True
    ChangeTokenStart: Optional[str] = None
    ChangeTokenEnd: Optional[str] = None
    DeleteObject: bool = True
    RoleAssignmentAdd: bool = True
    RoleAssignmentDelete: bool = True
    FetchLimit: Optional[str] = None
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
