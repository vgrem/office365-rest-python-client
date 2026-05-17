from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudPcUserRoleScopeTagInfo(ClientValue):
    def __init__(self, display_name: str | None = None, role_scope_tag_id: str | None = None):
        self.displayName = display_name
        self.roleScopeTagId = role_scope_tag_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcUserRoleScopeTagInfo"
