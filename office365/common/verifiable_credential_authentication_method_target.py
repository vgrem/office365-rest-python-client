from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata


class VerifiableCredentialAuthenticationMethodTarget(Entity):
    @odata(name="verifiedIdProfiles")
    @property
    def verified_id_profiles(self) -> GuidCollection:
        """Gets the verifiedIdProfiles property"""
        return self.properties.get("verifiedIdProfiles", GuidCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VerifiableCredentialAuthenticationMethodTarget"
