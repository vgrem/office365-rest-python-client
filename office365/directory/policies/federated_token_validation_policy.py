from __future__ import annotations

from office365.directory.objects.object import DirectoryObject
from office365.directory.policies.validating_domains import ValidatingDomains
from office365.runtime.types.odata_property import odata


class FederatedTokenValidationPolicy(DirectoryObject):
    @odata(name="validatingDomains")
    @property
    def validating_domains(self) -> ValidatingDomains:
        """Gets the validatingDomains property"""
        return self.properties.get("validatingDomains", ValidatingDomains())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FederatedTokenValidationPolicy"
