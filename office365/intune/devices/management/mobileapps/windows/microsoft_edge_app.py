from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.microsoftedgechannel import (
        MicrosoftEdgeChannel,
    )


class WindowsMicrosoftEdgeApp(Entity):
    @odata(name="channel")
    @property
    def channel(self) -> MicrosoftEdgeChannel:
        """Gets the channel property"""
        from office365.intune.devices.compliance.microsoftedgechannel import (
            MicrosoftEdgeChannel,
        )

        return self.properties.get("channel", MicrosoftEdgeChannel.dev)

    @odata(name="displayLanguageLocale")
    @property
    def display_language_locale(self) -> Optional[str]:
        """Gets the displayLanguageLocale property"""
        return self.properties.get("displayLanguageLocale", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsMicrosoftEdgeApp"
