from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.teams.custom_app_settings import CustomAppSettings


class TeamsAppSettings(Entity):
    @odata(name="allowUserRequestsForAppAccess")
    @property
    def allow_user_requests_for_app_access(self) -> Optional[bool]:
        """Gets the allowUserRequestsForAppAccess property"""
        return self.properties.get("allowUserRequestsForAppAccess", None)

    @odata(name="isUserPersonalScopeResourceSpecificConsentEnabled")
    @property
    def is_user_personal_scope_resource_specific_consent_enabled(self) -> Optional[bool]:
        """Gets the isUserPersonalScopeResourceSpecificConsentEnabled property"""
        return self.properties.get("isUserPersonalScopeResourceSpecificConsentEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppSettings"

    @odata(name="customAppSettings", beta=True)
    @property
    def custom_app_settings(self) -> Optional[CustomAppSettings]:
        """Gets the customAppSettings property"""
        return self.properties.get("customAppSettings", None)

    @odata(name="isChatResourceSpecificConsentEnabled", beta=True)
    @property
    def is_chat_resource_specific_consent_enabled(self) -> Optional[bool]:
        """Gets the isChatResourceSpecificConsentEnabled property"""
        return self.properties.get("isChatResourceSpecificConsentEnabled", None)
