from __future__ import annotations

from dataclasses import field

from office365.intune.devices.configurations.ios.home_screen_app import IosHomeScreenApp
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class IosHomeScreenFolderPage(ClientValue):
    apps: ClientValueCollection[IosHomeScreenApp] = field(
        default_factory=lambda: ClientValueCollection(IosHomeScreenApp)
    )
    displayName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosHomeScreenFolderPage"
