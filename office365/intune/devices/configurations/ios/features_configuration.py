from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.configurations.ios.home_screen_item import IosHomeScreenItem
from office365.intune.devices.configurations.ios.home_screen_page import IosHomeScreenPage
from office365.intune.devices.configurations.ios.notification_settings import IosNotificationSettings
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class IosDeviceFeaturesConfiguration(Entity):
    @odata(name="assetTagTemplate")
    @property
    def asset_tag_template(self) -> Optional[str]:
        """Gets the assetTagTemplate property"""
        return self.properties.get("assetTagTemplate", None)

    @odata(name="homeScreenDockIcons")
    @property
    def home_screen_dock_icons(self) -> ClientValueCollection[IosHomeScreenItem]:
        """Gets the homeScreenDockIcons property"""
        return self.properties.get("homeScreenDockIcons", ClientValueCollection[IosHomeScreenItem](IosHomeScreenItem))

    @odata(name="homeScreenPages")
    @property
    def home_screen_pages(self) -> ClientValueCollection[IosHomeScreenPage]:
        """Gets the homeScreenPages property"""
        return self.properties.get("homeScreenPages", ClientValueCollection[IosHomeScreenPage](IosHomeScreenPage))

    @odata(name="lockScreenFootnote")
    @property
    def lock_screen_footnote(self) -> Optional[str]:
        """Gets the lockScreenFootnote property"""
        return self.properties.get("lockScreenFootnote", None)

    @odata(name="notificationSettings")
    @property
    def notification_settings(self) -> ClientValueCollection[IosNotificationSettings]:
        """Gets the notificationSettings property"""
        return self.properties.get(
            "notificationSettings", ClientValueCollection[IosNotificationSettings](IosNotificationSettings)
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosDeviceFeaturesConfiguration"
