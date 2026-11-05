from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class RoleAssignmentResourcePayload(ClientValue):
    directoryScopeId: Optional[str] = None
    principalId: Optional[str] = None
    roleDefinitionId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.Events.RoleAssignmentResourcePayload"
