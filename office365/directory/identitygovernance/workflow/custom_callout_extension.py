from typing import Optional

from office365.directory.extensions.custom.clientconfiguration import CustomExtensionClientConfiguration
from office365.directory.extensions.custom.customextensionendpointconfiguration import (
    CustomExtensionEndpointConfiguration,
)
from office365.directory.identitygovernance.customextensionauthenticationconfiguration import (
    CustomExtensionAuthenticationConfiguration,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class CustomCalloutExtension(Entity):
    """An abstract type that defines the configuration for apps that can extend the customer's identity flows."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Display name for the customCalloutExtension object."""
        return self.properties.get("displayName", None)

    @odata(name="authenticationConfiguration")
    @property
    def authentication_configuration(self) -> CustomExtensionAuthenticationConfiguration:
        """Gets the authenticationConfiguration property"""
        return self.properties.get("authenticationConfiguration", CustomExtensionAuthenticationConfiguration())

    @odata(name="clientConfiguration")
    @property
    def client_configuration(self) -> CustomExtensionClientConfiguration:
        """Gets the clientConfiguration property"""
        return self.properties.get("clientConfiguration", CustomExtensionClientConfiguration())

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="endpointConfiguration")
    @property
    def endpoint_configuration(self) -> CustomExtensionEndpointConfiguration:
        """Gets the endpointConfiguration property"""
        return self.properties.get("endpointConfiguration", CustomExtensionEndpointConfiguration())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomCalloutExtension"
