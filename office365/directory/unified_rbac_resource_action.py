from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UnifiedRbacResourceAction(Entity):
    @odata(name="actionVerb")
    @property
    def action_verb(self) -> Optional[str]:
        """Gets the actionVerb property"""
        return self.properties.get("actionVerb", None)

    @odata(name="authenticationContextId")
    @property
    def authentication_context_id(self) -> Optional[str]:
        """Gets the authenticationContextId property"""
        return self.properties.get("authenticationContextId", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="isAuthenticationContextSettable")
    @property
    def is_authentication_context_settable(self) -> Optional[bool]:
        """Gets the isAuthenticationContextSettable property"""
        return self.properties.get("isAuthenticationContextSettable", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="resourceScopeId")
    @property
    def resource_scope_id(self) -> Optional[str]:
        """Gets the resourceScopeId property"""
        return self.properties.get("resourceScopeId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRbacResourceAction"
