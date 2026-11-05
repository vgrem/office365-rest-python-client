from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudPcUserRoleScopeTagInfo(ClientValue):
    displayName: str | None = None
    roleScopeTagId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcUserRoleScopeTagInfo"
