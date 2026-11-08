from __future__ import annotations

from office365.directory.extensions.custom.customextensionendpointconfiguration import (  # noqa: E501
    CustomExtensionEndpointConfiguration,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class CustomDataProvidedResource(Entity):
    @odata(name="notificationEndpointConfiguration")
    @property
    def notification_endpoint_configuration(self) -> CustomExtensionEndpointConfiguration:
        """Gets the notificationEndpointConfiguration property"""
        return self.properties.get("notificationEndpointConfiguration", CustomExtensionEndpointConfiguration())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomDataProvidedResource"
