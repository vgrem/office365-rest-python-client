from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.identities.providers.saml_or_wsfed import SamlOrWsFedProvider
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.providers.external_domain_name import ExternalDomainName


class SamlOrWsFedExternalDomainFederation(SamlOrWsFedProvider):
    @odata(name="domains", navigation=True)
    @property
    def domains(self) -> EntityCollection[ExternalDomainName]:
        """Gets the domains property"""
        from office365.directory.identities.providers.external_domain_name import ExternalDomainName

        return self.properties.get(
            "domains",
            EntityCollection[ExternalDomainName](
                self.context, ExternalDomainName, ResourcePath("domains", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SamlOrWsFedExternalDomainFederation"
