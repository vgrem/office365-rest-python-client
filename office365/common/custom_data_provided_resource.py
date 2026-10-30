from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.extensions.custom.customextensionendpointconfiguration import (
        CustomExtensionEndpointConfiguration,
    )


class CustomDataProvidedResource(Entity):
    @odata(name="notificationEndpointConfiguration")
    @property
    def notification_endpoint_configuration(self) -> CustomExtensionEndpointConfiguration:
        """Gets the notificationEndpointConfiguration property"""
        from office365.directory.extensions.custom.customextensionendpointconfiguration import (
            CustomExtensionEndpointConfiguration,
        )

        return self.properties.get("notificationEndpointConfiguration", CustomExtensionEndpointConfiguration())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomDataProvidedResource"
