from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata


class PasskeyAuthenticationMethodTarget(Entity):
    @odata(name="allowedPasskeyProfiles")
    @property
    def allowed_passkey_profiles(self) -> GuidCollection:
        """Gets the allowedPasskeyProfiles property"""
        return self.properties.get("allowedPasskeyProfiles", GuidCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PasskeyAuthenticationMethodTarget"
