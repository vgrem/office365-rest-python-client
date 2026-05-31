from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.attributecollection.page_view_configuration import (
    AuthenticationAttributeCollectionPageViewConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationAttributeCollectionPage(ClientValue):
    views: ClientValueCollection[AuthenticationAttributeCollectionPageViewConfiguration] = field(
        default_factory=lambda: ClientValueCollection(AuthenticationAttributeCollectionPageViewConfiguration)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAttributeCollectionPage"
