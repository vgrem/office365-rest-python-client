from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.microsoftedgechannel import MicrosoftEdgeChannel
from office365.runtime.types.odata_property import odata


class WindowsMicrosoftEdgeApp(Entity):
    @odata(name="channel")
    @property
    def channel(self) -> MicrosoftEdgeChannel:
        """Gets the channel property"""
        return self.properties.get("channel", MicrosoftEdgeChannel.dev)

    @odata(name="displayLanguageLocale")
    @property
    def display_language_locale(self) -> Optional[str]:
        """Gets the displayLanguageLocale property"""
        return self.properties.get("displayLanguageLocale", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsMicrosoftEdgeApp"
