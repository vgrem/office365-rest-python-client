from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.identities.userflows.user_flow_api_connector_configuration import (  # noqa: E501
    UserFlowApiConnectorConfiguration,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.provider import IdentityProvider
    from office365.directory.identities.providers.base import IdentityProviderBase
    from office365.directory.identities.userflows.language_configuration import (
        UserFlowLanguageConfiguration,
    )
    from office365.directory.identities.userflows.user_attribute_assignment import (
        IdentityUserFlowAttributeAssignment,
    )


class B2xIdentityUserFlow(Entity):
    @odata(name="apiConnectorConfiguration")
    @property
    def api_connector_configuration(self) -> UserFlowApiConnectorConfiguration:
        """Gets the apiConnectorConfiguration property"""
        return self.properties.get("apiConnectorConfiguration", UserFlowApiConnectorConfiguration())

    @odata(name="identityProviders", navigation=True)
    @property
    def identity_providers(self) -> EntityCollection[IdentityProvider]:
        """Gets the identityProviders property"""
        from office365.directory.identities.provider import IdentityProvider

        return self.properties.get(
            "identityProviders",
            EntityCollection[IdentityProvider](
                self.context, IdentityProvider, ResourcePath("identityProviders", self.resource_path)
            ),
        )

    @odata(name="languages", navigation=True)
    @property
    def languages(self) -> EntityCollection[UserFlowLanguageConfiguration]:
        """Gets the languages property"""
        from office365.directory.identities.userflows.language_configuration import (
            UserFlowLanguageConfiguration,
        )

        return self.properties.get(
            "languages",
            EntityCollection[UserFlowLanguageConfiguration](
                self.context, UserFlowLanguageConfiguration, ResourcePath("languages", self.resource_path)
            ),
        )

    @odata(name="userAttributeAssignments", navigation=True)
    @property
    def user_attribute_assignments(self) -> EntityCollection[IdentityUserFlowAttributeAssignment]:
        """Gets the userAttributeAssignments property"""
        from office365.directory.identities.userflows.user_attribute_assignment import (
            IdentityUserFlowAttributeAssignment,
        )

        return self.properties.get(
            "userAttributeAssignments",
            EntityCollection[IdentityUserFlowAttributeAssignment](
                self.context,
                IdentityUserFlowAttributeAssignment,
                ResourcePath("userAttributeAssignments", self.resource_path),
            ),
        )

    @odata(name="userFlowIdentityProviders", navigation=True)
    @property
    def user_flow_identity_providers(self) -> EntityCollection[IdentityProviderBase]:
        """Gets the userFlowIdentityProviders property"""
        from office365.directory.identities.providers.base import IdentityProviderBase

        return self.properties.get(
            "userFlowIdentityProviders",
            EntityCollection[IdentityProviderBase](
                self.context, IdentityProviderBase, ResourcePath("userFlowIdentityProviders", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.B2xIdentityUserFlow"
