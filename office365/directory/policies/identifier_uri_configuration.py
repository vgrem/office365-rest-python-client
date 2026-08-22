from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.identifier_uri_restriction import IdentifierUriRestriction
from office365.runtime.client_value import ClientValue


@dataclass
class IdentifierUriConfiguration(ClientValue):
    nonDefaultUriAddition: IdentifierUriRestriction = field(default_factory=IdentifierUriRestriction)
    uriAdditionWithoutUniqueTenantIdentifier: IdentifierUriRestriction = field(default_factory=IdentifierUriRestriction)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdentifierUriConfiguration"
