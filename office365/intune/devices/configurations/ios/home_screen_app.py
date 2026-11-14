from __future__ import annotations

from office365.intune.devices.configurations.ios.home_screen_item import IosHomeScreenItem


class IosHomeScreenApp(IosHomeScreenItem):
    bundleID: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosHomeScreenApp"
