from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.attributecollection.page import AuthenticationAttributeCollectionPage
from office365.directory.identities.userflows.attribute import IdentityUserFlowAttribute
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


@dataclass
class OnAttributeCollectionExternalUsersSelfServiceSignUp(ClientValue):
    attributeCollectionPage: AuthenticationAttributeCollectionPage = field(
        default_factory=AuthenticationAttributeCollectionPage
    )
    attributes: EntityCollection[IdentityUserFlowAttribute] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnAttributeCollectionExternalUsersSelfServiceSignUp"
