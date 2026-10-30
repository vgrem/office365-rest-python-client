from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.validating_domains import ValidatingDomains


class FederatedTokenValidationPolicy(Entity):
    @odata(name="validatingDomains")
    @property
    def validating_domains(self) -> ValidatingDomains:
        """Gets the validatingDomains property"""
        from office365.directory.policies.validating_domains import ValidatingDomains

        return self.properties.get("validatingDomains", ValidatingDomains())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FederatedTokenValidationPolicy"
